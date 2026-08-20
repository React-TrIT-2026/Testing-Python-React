export function StudioHeader({ summary }) {
  return (
    <>
      <header className="topbar">
        <p className="wordmark">
          <span className="wordmark__mark" aria-hidden="true">
            NZ
          </span>
          Naiz Studio
          <span className="wordmark__sub">Reservas</span>
        </p>
      </header>

      <section className="hero">
        <p className="hero__eyebrow">Cuadrante de clases dirigidas</p>
        <h1 className="hero__title">
          Coge tu sitio <em>antes</em> de que se llene.
        </h1>
        <dl className="hero__stats">
          <div className="stat">
            <dt className="stat__label">clases en el cuadrante</dt>
            <dd className="stat__value">{summary.classCount}</dd>
          </div>
          <div className="stat">
            <dt className="stat__label">con plaza libre</dt>
            <dd className="stat__value">{summary.openCount}</dd>
          </div>
          <div className="stat">
            <dt className="stat__label">reservas tuyas</dt>
            <dd className="stat__value">{summary.myBookings}</dd>
          </div>
        </dl>
      </section>
    </>
  );
}
