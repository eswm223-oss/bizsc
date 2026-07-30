import { useEffect, useState } from "react";
import { getHealth } from "../api/health";

function HomePage() {
  const [status, setStatus] = useState<string>("loading...");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHealth() {
      try {
        const health = await getHealth();
        setStatus(health.status);
      } catch (e) {
        //setError("APIとの通信に失敗しました");
        if (e instanceof Error) {
          setError(e.message);
        }
      }
    }

    fetchHealth();
  }, []);

  return (
    <div>
      <h1>Home</h1>

      {error ? <p>{error}</p> : <p>API status: {status}</p>}
    </div>
  );
}

export default HomePage;
