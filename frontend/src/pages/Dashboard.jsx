import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div>
      <h2>Dashboard</h2>

      <button className="primary-btn">
        Record Exercise
      </button>

      <div style={{ marginTop: 20, color: "#b3b3b3" }}>
        This week summary will go here
      </div>
    </div>
  );
}