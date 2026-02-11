export const resources = {
  units: {
    title: 'Unidades',
    endpoint: '/units/',
    fields: [
      { name: 'code', label: 'Código', required: true },
      { name: 'block', label: 'Bloco' },
    ],
  },
  residents: {
    title: 'Moradores',
    endpoint: '/residents/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'phone', label: 'Telefone' },
      { name: 'unit', label: 'ID Unidade', required: true, type: 'number' },
    ],
  },
  visitors: {
    title: 'Visitantes',
    endpoint: '/visitors/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'document', label: 'Documento', required: true },
      { name: 'unit', label: 'ID Unidade', type: 'number' },
    ],
  },
  visitLogs: {
    title: 'Logs de Visita',
    endpoint: '/visit-logs/',
    fields: [
      { name: 'visitor', label: 'ID Visitante', required: true, type: 'number' },
      { name: 'entry_at', label: 'Entrada (ISO)', required: true },
      { name: 'exit_at', label: 'Saída (ISO)' },
      { name: 'notes', label: 'Observações' },
    ],
  },
  packages: {
    title: 'Encomendas',
    endpoint: '/packages/',
    fields: [
      { name: 'description', label: 'Descrição', required: true },
      { name: 'unit', label: 'ID Unidade', required: true, type: 'number' },
    ],
  },
  announcements: {
    title: 'Comunicados',
    endpoint: '/announcements/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'content', label: 'Conteúdo', required: true },
    ],
  },
  incidents: {
    title: 'Ocorrências',
    endpoint: '/incidents/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'description', label: 'Descrição', required: true },
      { name: 'status', label: 'Status' },
    ],
  },
  commonAreas: {
    title: 'Áreas Comuns',
    endpoint: '/common-areas/',
    fields: [
      { name: 'name', label: 'Nome', required: true },
      { name: 'description', label: 'Descrição' },
    ],
  },
  reservations: {
    title: 'Reservas',
    endpoint: '/reservations/',
    fields: [
      { name: 'common_area', label: 'ID Área Comum', required: true, type: 'number' },
      { name: 'unit', label: 'ID Unidade', required: true, type: 'number' },
      { name: 'start_at', label: 'Início (ISO)', required: true },
      { name: 'end_at', label: 'Fim (ISO)', required: true },
      { name: 'status', label: 'Status' },
    ],
  },
}
