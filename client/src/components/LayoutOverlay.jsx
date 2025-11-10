/**
 * 布局叠加层组件：在PDF上显示文本块的位置
 * @param {Object} props
 * @param {Array} props.layout - 布局数据数组
 * @param {number} props.page - 当前页码
 * @param {number} props.scale - 缩放比例（需与PdfViewer一致）
 * @param {Function} props.onBlockClick - 点击文本块的回调
 */
export default function LayoutOverlay({ layout = [], page, scale = 1.2, onBlockClick }) {
  if (!layout || layout.length === 0) {
    console.log('LayoutOverlay: layout为空')
    return null
  }

  // 过滤当前页的文本块
  const pageBlocks = layout.filter(b => {
    const blockPage = b.page !== undefined ? b.page : (b.page_no || 0)
    return blockPage === page
  })
  
  console.log(`LayoutOverlay: 第${page}页有${pageBlocks.length}个文本块`)

  return (
    <div className="absolute top-0 left-0 pointer-events-none w-full h-full" style={{ zIndex: 10 }}>
      {pageBlocks.map((block, i) => {
        const [x0, y0, x1, y1] = block.bbox || [0, 0, 0, 0]
        const width = (x1 - x0) * scale
        const height = (y1 - y0) * scale

        return (
          <div
            key={`block-${i}-${block.text?.substring(0, 10)}`}
            className="pointer-events-auto cursor-pointer hover:bg-yellow-300 transition-all duration-200"
            style={{
              position: "absolute",
              left: `${x0 * scale}px`,
              top: `${y0 * scale}px`,
              width: `${Math.max(0, width)}px`,
              height: `${Math.max(0, height)}px`,
              backgroundColor: block.type === 'title' 
                ? "rgba(255, 200, 0, 0.3)" 
                : "rgba(255, 230, 0, 0.25)",
              border: block.type === 'title'
                ? "2px solid rgba(255, 180, 0, 0.7)"
                : "1px solid rgba(255, 200, 0, 0.5)",
              borderRadius: "2px",
            }}
            title={block.text || block.translated_text || ""}
            onClick={() => onBlockClick && onBlockClick(block)}
          />
        )
      })}
    </div>
  )
}

