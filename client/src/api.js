/**
 * API客户端：封装所有后端API调用
 */

const API_BASE = '/api'

/**
 * 上传文件
 * @param {File} file - 要上传的文件
 * @returns {Promise<Object>} 响应数据
 */
export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  })
  
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '上传失败')
  }
  return data.data
}

/**
 * 通过MinerU API解析PDF文件
 * @param {File} pdfFile - PDF文件
 * @param {boolean} wait - 是否等待任务完成（默认: false，返回task_id）
 * @returns {Promise<Object>} 包含task_id或解析结果的响应
 */
export async function parsePdfWithApi(pdfFile, wait = false) {
  const formData = new FormData()
  formData.append('file', pdfFile)
  formData.append('wait', wait.toString())
  
  const response = await fetch(`${API_BASE}/parse-pdf`, {
    method: 'POST',
    body: formData
  })
  
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '解析失败')
  }
  return data.data
}

/**
 * 查询MinerU解析任务状态
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} 任务状态和结果
 */
export async function getTaskStatus(taskId) {
  const response = await fetch(`${API_BASE}/task/${taskId}`)
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '查询失败')
  }
  return data.data
}

/**
 * 查询MinerU批量解析任务状态
 * @param {string} batchId - 批量任务ID
 * @returns {Promise<Object>} 批量任务状态和结果
 */
export async function getBatchStatus(batchId) {
  const response = await fetch(`${API_BASE}/batch/${batchId}`)
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '查询失败')
  }
  return data.data
}

/**
 * 解析MinerU JSON文件，生成layout（兼容旧接口）
 * @param {string} filename - JSON文件名
 * @param {File} file - 可选：上传的JSON文件
 * @returns {Promise<Object>} 包含layout数据的响应
 */
export async function parseLayout(filename = null, file = null) {
  const formData = new FormData()
  if (filename) {
    formData.append('filename', filename)
  }
  if (file) {
    formData.append('file', file)
  }
  
  const response = await fetch(`${API_BASE}/layout`, {
    method: 'POST',
    body: formData
  })
  
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '解析失败')
  }
  return data.data
}

/**
 * 翻译layout数组中的文本块
 * @param {Array} layout - layout数组
 * @param {string} targetLang - 目标语言（默认: zh）
 * @param {string} model - 使用的模型（可选）
 * @param {boolean} forceRetranslate - 是否强制重新翻译所有文本块（默认: false）
 * @returns {Promise<Object>} 翻译结果，包含更新后的layout
 */
export async function translateLayout(layout, targetLang = 'zh', model = null, forceRetranslate = false) {
  const response = await fetch(`${API_BASE}/translate-layout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      layout: layout,
      target_lang: targetLang,
      model: model,
      force_retranslate: forceRetranslate
    })
  })
  
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '翻译失败')
  }
  return data.data
}

/**
 * 翻译MinerU JSON文件
 * @param {string} filename - JSON文件名
 * @param {string} targetLang - 目标语言（默认: zh）
 * @param {string} model - 使用的模型（可选）
 * @param {File} file - 可选：上传的JSON文件
 * @returns {Promise<Object>} 翻译结果
 */
export async function translateDocument(filename = null, targetLang = 'zh', model = null, file = null) {
  const formData = new FormData()
  if (filename) {
    formData.append('filename', filename)
  }
  formData.append('target_lang', targetLang)
  if (model) {
    formData.append('model', model)
  }
  if (file) {
    formData.append('file', file)
  }
  
  const response = await fetch(`${API_BASE}/translate`, {
    method: 'POST',
    body: formData
  })
  
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '翻译失败')
  }
  return data.data
}

/**
 * 获取文件URL
 * @param {string} filename - 文件名
 * @param {string} type - 文件类型：'files' 或 'mineru'
 * @returns {string} 文件URL
 */
export function getFileUrl(filename, type = 'files') {
  return `${API_BASE}/${type}/${filename}`
}

/**
 * 获取全文Markdown内容
 * @param {string} taskId - 任务ID或batch_id
 * @returns {Promise<Object>} 包含content的响应
 */
export async function getFullText(taskId) {
  const response = await fetch(`${API_BASE}/full-text/${taskId}`)
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.message || '获取全文失败')
  }
  return data.data
}

/**
 * 获取图片URL
 * @param {string} taskId - 任务ID或batch_id
 * @param {string} imageName - 图片文件名
 * @returns {string} 图片URL
 */
export function getImageUrl(taskId, imageName) {
  return `${API_BASE}/images/${taskId}/${imageName}`
}

