{{- define "blog-platform.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "blog-platform.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "blog-platform.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
