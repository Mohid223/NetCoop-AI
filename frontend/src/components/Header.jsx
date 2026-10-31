function Header() {
  return (
    <header className="top-header">
      <div className="welcome">
        <h1>
          Welcome Back, Admin! <span className="wave">👋</span>
        </h1>
        <p>Here's your network status at a glance</p>
      </div>
      <div className="header-right">
        <div className="online-chip">
          <span className="dot"></span> Online
        </div>
        <div className="avatar">A</div>
      </div>
    </header>
  );
}

export default Header;