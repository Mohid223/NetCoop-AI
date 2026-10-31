const navigation = [
  { id: "overview", label: "Overview", icon: "⌂" },
  { id: "diagnosis", label: "Diagnosis", icon: "⌕" },
  { id: "evidence", label: "Evidence", icon: "◈" },
  { id: "chat", label: "AI Assistant", icon: "✧" },
  { id: "json", label: "JSON Report", icon: "{}" },
];

function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-heading">WORKSPACE</div>

      <nav className="sidebar-nav">
        {navigation.map((item) => (
          <button
            key={item.id}
            className={`sidebar-link ${
              activeTab === item.id ? "active" : ""
            }`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-icon">AI</div>
        <div>
          <strong>NetCoop Engine</strong>
          <p>Autonomous diagnosis</p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;