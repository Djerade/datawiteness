import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";

export const useHealth = () =>
  useQuery({ queryKey: ["health"], queryFn: () => api<{ status: string }>("/health") });
