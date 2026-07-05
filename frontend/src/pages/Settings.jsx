export default function Settings() {
  return (
    <div>
      <h2>Settings</h2>

      <section>
        <h3>Units</h3>
        <select className="select">
          <option value="imperial">Imperial (lb)</option>
          <option value="metric">Metric (kg)</option>
        </select>
      </section>

      <section style={{ marginTop: 20 }}>
        <h3>Theme</h3>
        <select className="select">
          <option value="dark">Dark</option>
          <option value="light">Light</option>
        </select>
      </section>

      <section style={{ marginTop: 20 }}>
        <h3>Time Zone</h3>
        <select className="select">
          <option value="America/Chicago">Central (Chicago)</option>
          <option value="America/New_York">Eastern (New York)</option>
          <option value="America/Los_Angeles">Pacific (LA)</option>
        </select>
      </section>
    </div>
  );
}