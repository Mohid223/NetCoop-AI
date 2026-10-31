function AffectedDevices({ devices = [] }) {
  const deviceList = Array.isArray(devices) ? devices : [];

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <h2>Affected Devices</h2>
          <p>Devices identified during network investigation</p>
        </div>
        <span className="count-badge">{deviceList.length}</span>
      </div>

      {deviceList.length > 0 ? (
        <div className="device-list">
          {deviceList.map((device, index) => {
            const name =
              typeof device === "string"
                ? device
                : device.name || device.hostname || device.device_id || `Device ${index + 1}`;

            const address =
              typeof device === "object"
                ? device.ip_address || device.ip || "IP unavailable"
                : "Device identified";

            return (
              <div className="device-item" key={index}>
                <div className="device-icon">▣</div>
                <div className="device-info">
                  <strong>{name}</strong>
                  <span>{address}</span>
                </div>
                <span className="device-status">Identified</span>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">
          <span className="empty-icon">✓</span>
          <p>No affected devices identified.</p>
          <small>More telemetry may be required.</small>
        </div>
      )}
    </section>
  );
}

export default AffectedDevices;