function AffectedDevices({ devices = [] }) {
  return (
    <div className="card affected-devices">
      <div className="card-header">
        <h3>Affected Devices</h3>
        <span className="badge">
          {devices.length} Device{devices.length !== 1 ? "s" : ""}
        </span>
      </div>

      {devices.length > 0 ? (
        devices.map((device) => (
          <div key={device} className="device-row">
            <div className="device-icon">🖥️</div>
            <div>
              <div className="device-name">{device}</div>
              <div className="device-role">Network Device</div>
            </div>
            <span className="chevron">›</span>
          </div>
        ))
      ) : (
        <p className="text-muted">No specific devices identified.</p>
      )}
    </div>
  );
}

export default AffectedDevices;