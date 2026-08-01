import { Fragment } from 'react'

// Deliberately renders text nodes only; markdown input is never injected as HTML.
export default function MarkdownContent({ content }: { content: string }) {
  return <div className="markdown-content">{content.split(/\n{2,}/).map((block, index) => {
    const trimmed = block.trim()
    if (trimmed.startsWith('### ')) return <h3 key={index}>{trimmed.slice(4)}</h3>
    if (trimmed.startsWith('## ')) return <h2 key={index}>{trimmed.slice(3)}</h2>
    if (trimmed.startsWith('# ')) return <h1 key={index}>{trimmed.slice(2)}</h1>
    if (trimmed.startsWith('```')) return <pre key={index}><code>{trimmed.replace(/^```\w*\n?|```$/g, '')}</code></pre>
    if (trimmed.split('\n').every((line) => /^[-*] /.test(line))) return <ul key={index}>{trimmed.split('\n').map((line, item) => <li key={item}>{line.slice(2)}</li>)}</ul>
    return <Fragment key={index}><p>{trimmed}</p></Fragment>
  })}</div>
}
