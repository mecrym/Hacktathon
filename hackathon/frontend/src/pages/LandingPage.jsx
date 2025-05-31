import { useState } from "react";

const LandingPage = () => {
  const [mensagem, setMensagem] = useState("");

  return (
    <div className="container text-center mt-5">
      <h1>Bem-vindo ao Sistema de Cadastro</h1>
      <p className="lead">Faça seu cadastro ou login para continuar</p>
      {mensagem && <div className="alert alert-info">{mensagem}</div>}
      <div className="mt-4">
        <a href="/cadastro" className="btn btn-primary me-2">Cadastro</a>
        <a href="/login" className="btn btn-secondary">Login</a>
      </div>
    </div>
  );
}