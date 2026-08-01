import type { InputHTMLAttributes } from 'react'

export default function Input({ label, error, id, ...props }: InputHTMLAttributes<HTMLInputElement> & { label: string; error?: string }) {
  const inputId = id || props.name
  return <label className="ui-input"><span>{label}</span><input id={inputId} {...props} />{error ? <small>{error}</small> : null}</label>
}
