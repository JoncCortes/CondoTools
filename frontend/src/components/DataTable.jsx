export function DataTable({ fields, rows, onEdit }) {
  return (
    <table>
      <thead>
        <tr>
          {fields.map((f) => <th key={f.name}>{f.label}</th>)}
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            {fields.map((f) => <td key={f.name}>{String(row[f.name] ?? '')}</td>)}
            <td><button onClick={() => onEdit(row)}>Editar</button></td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
