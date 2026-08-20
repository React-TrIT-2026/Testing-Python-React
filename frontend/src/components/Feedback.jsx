export function Feedback({ feedback, onDismiss }) {
  if (!feedback) return null;

  return (
    <div className="toasts">
      <div
        className={`notice notice--${feedback.tone}`}
        role={feedback.tone === "error" ? "alert" : "status"}
      >
        <p>{feedback.message}</p>
        <button type="button" className="btn btn--ghost" onClick={onDismiss}>
          Cerrar
        </button>
      </div>
    </div>
  );
}
