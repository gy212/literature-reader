"""
MinerU API调用模块：通过API调用MinerU服务解析PDF
根据MinerU官方API文档实现
"""
import json
import logging
import requests
import time
import zipfile
import io
from typing import Dict, Any, Optional, List
from flask import current_app, url_for
from pathlib import Path

logger = logging.getLogger(__name__)


def get_mineru_headers() -> Dict[str, str]:
    """
    获取MinerU API请求头
    
    Returns:
        包含Authorization的请求头
    """
    token = current_app.config.get('MINERU_TOKEN', '')
    if not token:
        raise ValueError("未配置MINERU_TOKEN，请在环境变量中设置")
    
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def create_extract_task(file_url: str, model_version: str = None, **kwargs) -> Dict[str, Any]:
    """
    创建MinerU解析任务（通过文件URL）
    
    Args:
        file_url: 文件URL（必须是可公开访问的URL）
        model_version: 模型版本（pipeline 或 vlm，默认从配置读取）
        **kwargs: 其他可选参数（is_ocr, enable_formula, enable_table, language, data_id等）
    
    Returns:
        包含task_id的响应数据
    """
    try:
        base_url = current_app.config.get('MINERU_BASE_URL', 'https://mineru.net/api/v4')
        api_url = f"{base_url}/extract/task"
        
        if not model_version:
            model_version = current_app.config.get('MINERU_MODEL_VERSION', 'vlm')
        
        headers = get_mineru_headers()
        
        # 构建请求体
        data = {
            "url": file_url,
            "model_version": model_version
        }
        
        # 添加可选参数
        optional_params = ['is_ocr', 'enable_formula', 'enable_table', 'language', 
                         'data_id', 'callback', 'seed', 'extra_formats', 'page_ranges']
        for param in optional_params:
            if param in kwargs:
                data[param] = kwargs[param]
        
        logger.info(f"创建MinerU解析任务: {file_url}")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        # 检查响应
        response.raise_for_status()
        result = response.json()
        
        # 检查业务状态码
        if result.get('code') != 0:
            error_msg = result.get('msg', '未知错误')
            logger.error(f"MinerU API返回错误: {error_msg}")
            raise Exception(f"MinerU API错误: {error_msg}")
        
        task_id = result.get('data', {}).get('task_id')
        if not task_id:
            raise Exception("未获取到task_id")
        
        logger.info(f"任务创建成功，task_id: {task_id}")
        return result.get('data', {})
        
    except requests.exceptions.RequestException as e:
        logger.error(f"MinerU API调用失败: {e}")
        raise Exception(f"MinerU API调用失败: {str(e)}")
    except Exception as e:
        logger.error(f"创建解析任务失败: {e}", exc_info=True)
        raise


def get_task_result(task_id: str) -> Dict[str, Any]:
    """
    查询MinerU解析任务结果
    
    Args:
        task_id: 任务ID
    
    Returns:
        任务状态和结果数据
    """
    try:
        base_url = current_app.config.get('MINERU_BASE_URL', 'https://mineru.net/api/v4')
        api_url = f"{base_url}/extract/task/{task_id}"
        
        headers = get_mineru_headers()
        
        logger.info(f"查询任务结果: {task_id}")
        response = requests.get(api_url, headers=headers, timeout=30)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') != 0:
            error_msg = result.get('msg', '未知错误')
            logger.error(f"MinerU API返回错误: {error_msg}")
            raise Exception(f"MinerU API错误: {error_msg}")
        
        return result.get('data', {})
        
    except requests.exceptions.RequestException as e:
        logger.error(f"查询任务结果失败: {e}")
        raise Exception(f"查询任务结果失败: {str(e)}")
    except Exception as e:
        logger.error(f"查询任务结果异常: {e}", exc_info=True)
        raise


def wait_for_task_completion(task_id: str, max_wait_time: int = 600, poll_interval: int = 5) -> Dict[str, Any]:
    """
    等待任务完成并返回结果
    
    Args:
        task_id: 任务ID
        max_wait_time: 最大等待时间（秒）
        poll_interval: 轮询间隔（秒）
    
    Returns:
        任务完成后的结果数据
    """
    start_time = time.time()
    
    while True:
        result = get_task_result(task_id)
        state = result.get('state', '')
        
        logger.info(f"任务状态: {state}, task_id: {task_id}")
        
        if state == 'done':
            logger.info(f"任务完成: {task_id}")
            return result
        elif state == 'failed':
            err_msg = result.get('err_msg', '解析失败')
            logger.error(f"任务失败: {err_msg}")
            raise Exception(f"解析失败: {err_msg}")
        elif state in ['pending', 'running', 'converting']:
            # 检查是否超时
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                raise Exception(f"任务超时（超过{max_wait_time}秒）")
            
            # 显示进度
            progress = result.get('extract_progress', {})
            if progress:
                extracted = progress.get('extracted_pages', 0)
                total = progress.get('total_pages', 0)
                logger.info(f"解析进度: {extracted}/{total} 页")
            
            # 等待后继续轮询
            time.sleep(poll_interval)
        else:
            logger.warning(f"未知任务状态: {state}")
            time.sleep(poll_interval)


def download_and_extract_zip(zip_url: str, extract_to: Path) -> Dict[str, Any]:
    """
    下载并解压MinerU返回的ZIP文件
    
    Args:
        zip_url: ZIP文件URL
        extract_to: 解压目标目录
    
    Returns:
        包含解压文件路径的字典
    """
    try:
        logger.info(f"下载ZIP文件: {zip_url}")
        response = requests.get(zip_url, timeout=300)
        response.raise_for_status()
        
        # 创建解压目录
        extract_to.mkdir(parents=True, exist_ok=True)
        
        # 解压ZIP文件
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(extract_to)
        
        logger.info(f"ZIP文件解压完成: {extract_to}")
        
        # 查找JSON文件，优先查找layout.json
        layout_json = extract_to / 'layout.json'
        full_md = extract_to / 'full.md'
        images_dir = extract_to / 'images'
        
        result = {
            "json_path": None,
            "extract_dir": str(extract_to),
            "full_md_path": str(full_md) if full_md.exists() else None,
            "images_dir": str(images_dir) if images_dir.exists() else None
        }
        
        if layout_json.exists():
            logger.info(f"找到layout.json: {layout_json}")
            result["json_path"] = str(layout_json)
            return result
        
        # 如果没有layout.json，查找其他JSON文件
        json_files = list(extract_to.rglob('*.json'))
        if json_files:
            # 优先查找包含"layout"或"model"的JSON文件
            for json_file in json_files:
                if 'layout' in json_file.name.lower() or 'model' in json_file.name.lower():
                    logger.info(f"找到JSON文件: {json_file}")
                    result["json_path"] = str(json_file)
                    return result
            # 否则使用第一个JSON文件
            json_path = json_files[0]
            logger.info(f"找到JSON文件: {json_path}")
            result["json_path"] = str(json_path)
            return result
        else:
            raise Exception("ZIP文件中未找到JSON文件")
            
    except Exception as e:
        logger.error(f"下载或解压ZIP文件失败: {e}", exc_info=True)
        raise


def get_file_upload_urls(files: List[Dict[str, str]], model_version: str = None) -> Dict[str, Any]:
    """
    批量获取文件上传URL
    
    Args:
        files: 文件列表，每个文件包含name和可选的data_id
        model_version: 模型版本
    
    Returns:
        包含batch_id和file_urls的响应数据
    """
    try:
        base_url = current_app.config.get('MINERU_BASE_URL', 'https://mineru.net/api/v4')
        api_url = f"{base_url}/file-urls/batch"
        
        if not model_version:
            model_version = current_app.config.get('MINERU_MODEL_VERSION', 'vlm')
        
        headers = get_mineru_headers()
        
        data = {
            "files": files,
            "model_version": model_version
        }
        
        logger.info(f"申请文件上传URL，文件数: {len(files)}")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') != 0:
            error_msg = result.get('msg', '未知错误')
            raise Exception(f"MinerU API错误: {error_msg}")
        
        return result.get('data', {})
        
    except Exception as e:
        logger.error(f"获取上传URL失败: {e}", exc_info=True)
        raise


def get_batch_task_result(batch_id: str) -> Dict[str, Any]:
    """
    批量查询MinerU解析任务结果
    
    Args:
        batch_id: 批量任务ID
    
    Returns:
        批量任务状态和结果数据
    """
    try:
        base_url = current_app.config.get('MINERU_BASE_URL', 'https://mineru.net/api/v4')
        api_url = f"{base_url}/extract-results/batch/{batch_id}"
        
        headers = get_mineru_headers()
        
        logger.info(f"查询批量任务结果: {batch_id}")
        response = requests.get(api_url, headers=headers, timeout=30)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') != 0:
            error_msg = result.get('msg', '未知错误')
            logger.error(f"MinerU API返回错误: {error_msg}")
            raise Exception(f"MinerU API错误: {error_msg}")
        
        return result.get('data', {})
        
    except requests.exceptions.RequestException as e:
        logger.error(f"查询批量任务结果失败: {e}")
        raise Exception(f"查询批量任务结果失败: {str(e)}")
    except Exception as e:
        logger.error(f"查询批量任务结果异常: {e}", exc_info=True)
        raise


def upload_file_to_url(file_path: str, upload_url: str) -> bool:
    """
    上传文件到指定的URL
    
    Args:
        file_path: 本地文件路径
        upload_url: 上传URL
    
    Returns:
        是否上传成功
    """
    try:
        logger.info(f"上传文件到: {upload_url}")
        with open(file_path, 'rb') as f:
            response = requests.put(upload_url, data=f, timeout=300)
            response.raise_for_status()
        
        logger.info(f"文件上传成功: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"文件上传失败: {e}", exc_info=True)
        raise Exception(f"文件上传失败: {str(e)}")


def parse_pdf_with_mineru_api(
    file_path: str, 
    file_url: str = None,
    wait_for_completion: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    通过MinerU API解析PDF文件（完整流程）
    
    Args:
        file_path: 本地文件路径（如果file_url为空，需要先上传）
        file_url: 文件URL（如果提供，直接使用；否则需要先上传获取URL）
        wait_for_completion: 是否等待任务完成
        **kwargs: 其他参数传递给create_extract_task
    
    Returns:
        解析结果数据
    """
    try:
        # 如果没有提供file_url，需要先上传文件
        if not file_url:
            # 这里需要实现文件上传逻辑
            # 由于MinerU需要可访问的URL，可能需要：
            # 1. 上传到云存储（OSS/S3等）
            # 2. 或者使用批量上传接口
            raise ValueError("当前版本需要提供file_url，或实现文件上传功能")
        
        # 创建解析任务
        task_data = create_extract_task(file_url, **kwargs)
        task_id = task_data.get('task_id')
        
        if not wait_for_completion:
            return {
                "task_id": task_id,
                "state": "pending",
                "message": "任务已提交，请使用task_id查询结果"
            }
        
        # 等待任务完成
        result = wait_for_task_completion(task_id)
        
        # 下载并解压结果
        zip_url = result.get('full_zip_url')
        if not zip_url:
            raise Exception("未获取到结果ZIP文件URL")
        
        # 解压到临时目录
        extract_dir = Path(current_app.config['MINERU_FOLDER']) / task_id
        zip_info = download_and_extract_zip(zip_url, extract_dir)
        
        # 读取JSON文件
        json_path = zip_info['json_path']
        with open(json_path, 'r', encoding='utf-8') as f:
            mineru_data = json.load(f)
        
        return {
            "task_id": task_id,
            "state": "done",
            "mineru_data": mineru_data,
            "json_path": json_path,
            "extract_dir": zip_info['extract_dir']
        }
        
    except Exception as e:
        logger.error(f"解析PDF失败: {e}", exc_info=True)
        raise
