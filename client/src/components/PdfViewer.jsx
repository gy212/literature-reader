import { useEffect, useRef, useState } from "react"
import * as pdfjsLib from "pdfjs-dist"

// 配置PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`

/**
 * PDF查看器组件
 * @param {Object} props
 * @param {string} props.fileUrl - PDF文件URL
 * @param {number} props.currentPage - 当前页码（从1开始）
 * @param {Function} props.onPageChange - 页码变化回调
 * @param {number} props.scale - 缩放比例
 */
export default function PdfViewer({ fileUrl, currentPage = 1, onPageChange, scale = 1.2 }) {
  const canvasRef = useRef(null)
  const [totalPages, setTotalPages] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!fileUrl) return

    let renderTask = null
    let isCancelled = false

    const renderPage = async () => {
      try {
        setLoading(true)
        setError(null)

        // 加载PDF文档
        const loadingTask = pdfjsLib.getDocument(fileUrl)
        const pdf = await loadingTask.promise
        
        if (isCancelled) return
        
        setTotalPages(pdf.numPages)

        // 渲染指定页面
        const page = await pdf.getPage(currentPage)
        const viewport = page.getViewport({ scale })

        const canvas = canvasRef.current
        if (!canvas || isCancelled) return

        const ctx = canvas.getContext("2d")
        
        // 清除之前的渲染
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        canvas.width = viewport.width
        canvas.height = viewport.height

        // 创建渲染任务
        renderTask = page.render({
          canvasContext: ctx,
          viewport: viewport
        })

        await renderTask.promise

        if (!isCancelled) {
          setLoading(false)
        }
      } catch (err) {
        if (!isCancelled) {
          console.error("PDF渲染错误:", err)
          setError(err.message)
          setLoading(false)
        }
      }
    }

    renderPage()

    // 清理函数：取消渲染任务
    return () => {
      isCancelled = true
      if (renderTask) {
        renderTask.cancel()
      }
    }
  }, [fileUrl, currentPage, scale])

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded">
        <p className="text-red-600">PDF加载失败: {error}</p>
      </div>
    )
  }

  return (
    <div className="relative inline-block">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75 z-30">
          <p className="text-gray-600">加载中...</p>
        </div>
      )}
      <canvas
        ref={canvasRef}
        className="border rounded shadow-sm bg-white block"
      />
      {totalPages > 0 && (
        <div className="mt-2 text-sm text-gray-600 text-center">
          第 {currentPage} 页 / 共 {totalPages} 页
        </div>
      )}
    </div>
  )
}

