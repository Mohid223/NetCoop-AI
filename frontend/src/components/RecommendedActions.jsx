function RecommendedActions({ actions = [] }) {
  return (
    <div className="card recommended-actions">
      <div className="card-header">
        <h3>Recommended Actions</h3>
      </div>

      {actions.length > 0 ? (
        <ul className="action-list">
          {actions.map((action, i) => (
            <li key={i}>
              <span className="check-circle">✓</span>
              <span>{action}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-muted">No recommended actions available.</p>
      )}
    </div>
  );
}

export default RecommendedActions;