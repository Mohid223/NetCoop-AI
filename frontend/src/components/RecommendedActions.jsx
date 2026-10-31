function RecommendedActions({ actions = [] }) {
  const actionList = Array.isArray(actions) ? actions : [];

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h2>Recommended Actions</h2>
          <p>Suggested next steps based on available evidence</p>
        </div>
        <span className="count-badge">{actionList.length}</span>
      </div>

      {actionList.length > 0 ? (
        <div className="action-list">
          {actionList.map((action, index) => {
            const title =
              typeof action === "string"
                ? action
                : action.title || action.action || action.description || `Action ${index + 1}`;

            const description =
              typeof action === "object"
                ? action.description || action.reason || ""
                : "";

            return (
              <div className="action-item" key={index}>
                <div className="action-number">{index + 1}</div>
                <div className="action-content">
                  <strong>{title}</strong>
                  {description && <p>{description}</p>}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">
          <p>No recommended actions available.</p>
        </div>
      )}

      <p className="safety-note">
        AI recommendations are advisory. Verify actions with your network
        administrator before making configuration changes.
      </p>
    </section>
  );
}

export default RecommendedActions;