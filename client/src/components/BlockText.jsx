/**
 * 文本块显示组件：支持原文/翻译/对照模式
 * @param {Object} props
 * @param {Object} props.block - 文本块数据
 * @param {string} props.mode - 显示模式：'original' | 'translated' | 'both'
 */
export default function BlockText({ block, mode = "both" }) {
  if (!block) return null

  const originalText = block.text || ""
  const translatedText = block.translated_text || ""

  return (
    <div className="p-3 bg-gray-50 rounded-lg border border-gray-200 my-2 hover:bg-gray-100 transition-colors">
      {mode === "original" && (
        <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
          {originalText}
        </p>
      )}
      {mode === "translated" && (
        <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
          {translatedText || originalText}
        </p>
      )}
      {mode === "both" && (
        <div>
          {translatedText ? (
            <>
              <div className="mb-3">
                <div className="text-xs font-semibold text-gray-500 mb-1">原文</div>
                <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
                  {originalText}
                </p>
              </div>
              <div className="pt-3 border-t border-gray-300">
                <div className="text-xs font-semibold text-gray-500 mb-1">翻译</div>
                <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
                  {translatedText}
                </p>
              </div>
            </>
          ) : (
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
              {originalText}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

