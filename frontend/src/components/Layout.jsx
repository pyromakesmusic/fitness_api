import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="app">
      <nav className="nav">
        <NavLink to="/dashboard" className="tab">
          Dashboard
        </NavLink>

        <NavLink to="/history" className="tab">
          History
        </NavLink>

        <NavLink to="/stats" className="tab">
          Stats
        </NavLink>

        <NavLink to="/settings" className="tab">
          Settings
        </NavLink>
      </nav>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}