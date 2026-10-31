function Header({ backendStatus = "checking" }) {
  const isOnline = backendStatus === "online";

  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="brand-logo">N</div>
        <div>
          <h2>NetCoop AI</h2>
          <p>Autonomous Network Intelligence</p>
        </div>
      </div>

      <div className="header-status">
        <span className={`status-dot ${isOnline ? "online" : "offline"}`} />
        <span>
          Backend:{" "}
          {backendStatus === "checking"
            ? "Checking..."
            : isOnline
              ? "Connected"
              : "Disconnected"}
        </span>
      </div>
    </header>
  );
}

export default Header;