import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      <header style={{ display: "flex", gap: 16, alignItems: "center" }}>
        <strong>DataWitness Africa</strong>
        <NavLink to="/">Tableau de bord</NavLink>
        <NavLink to="/sources">Sources</NavLink>
        <NavLink to="/divergences">Divergences</NavLink>
        <NavLink to="/graphe">Graphe</NavLink>
      </header>
      <main style={{ marginTop: 24 }}>
        <Outlet />
      </main>
    </div>
  );
}
