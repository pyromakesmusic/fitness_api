import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <nav style={{ display: "flex", gap: 10 }}>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/history">History</Link>
        <Link to="/stats">Stats</Link>
        <Link to="/settings">Settings</Link>
      </nav>

      <button style={{ marginTop: 20, fontSize: 20 }}>
        Record Exercise
      </button>
    </div>
  );
}