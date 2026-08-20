export function ScheduleSkeleton({ rows = 4 }) {
  return (
    <div aria-busy="true" aria-live="polite">
      <p className="visually-hidden">Cargando el horario</p>
      {Array.from({ length: rows }, (_, index) => (
        <div key={index} className="skeleton" />
      ))}
    </div>
  );
}
