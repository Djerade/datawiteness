import { useHealth } from "../hooks/useHealth";

export default function Dashboard() {
  const { data, isError } = useHealth();
  return (
    <section>
      <h1>Tableau de bord</h1>
      <p>API : {isError ? "injoignable" : (data?.status ?? "…")}</p>
      {/* TODO : compteurs sources / affirmations / divergences par verdict */}
    </section>
  );
}
