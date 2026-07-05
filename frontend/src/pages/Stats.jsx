import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const emptyData = [
  { day: "Mon", value: 0 },
  { day: "Tue", value: 0 },
  { day: "Wed", value: 0 },
  { day: "Thu", value: 0 },
  { day: "Fri", value: 0 },
  { day: "Sat", value: 0 },
  { day: "Sun", value: 0 },
];

export default function Stats() {
  return (
    <div>
      <h2>Stats</h2>

      <div style={{ width: "100%", height: 300, marginTop: 20 }}>
        <ResponsiveContainer>
          <LineChart data={emptyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#4ea1ff"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <p style={{ color: "#b3b3b3", marginTop: 12 }}>
        No workout data yet — this is where your progress will appear.
      </p>
    </div>
  );
}