import { Route, Routes } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import Sources from "./pages/Sources";
import Divergences from "./pages/Divergences";
import EvidencePage from "./pages/EvidencePage";
import GraphPage from "./pages/GraphPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="sources" element={<Sources />} />
        <Route path="divergences" element={<Divergences />} />
        <Route path="divergences/:id" element={<EvidencePage />} />
        <Route path="graphe" element={<GraphPage />} />
      </Route>
    </Routes>
  );
}
