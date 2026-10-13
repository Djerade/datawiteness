import { useParams } from "react-router-dom";

export default function EvidencePage() {
  const { id } = useParams();
  return (
    <section>
      <h1>Fiche de preuve</h1>
      <p>Comparaison {id}</p>
      {/* TODO : deux valeurs côte à côte, contrôles, explication, extraits, lien page source */}
    </section>
  );
}
