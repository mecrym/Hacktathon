import { useState } from 'react';

const Login = ({ setMensagem }) => {
  const [login, setLogin] = useState({ email: '', senha: '' });
  const usuarios = JSON.parse(localStorage.getItem('data.json')) || [];

  const handleLogin = (e) => {
    e.preventDefault();
    const usuario = usuarios.find(u => u.email === login.email);

    if (!usuario) {
      setMensagem('Usuário não encontrado');
    } else if (usuario.senha !== login.senha) {
      setMensagem('Senha incorreta');
    } else {
      setMensagem(`Bem-vindo, ${usuario.nome}!`);
    }

    setLogin({ email: '', senha: '' });
  };

  return (
    <form onSubmit={handleLogin} className="w-50 mx-auto mt-4">
      <h2>Login</h2>
      <input className="form-control mb-2" type="email" placeholder="Email" value={login.email} onChange={e => setLogin({ ...login, email: e.target.value })} required />
      <input className="form-control mb-2" type="password" placeholder="Senha" value={login.senha} onChange={e => setLogin({ ...login, senha: e.target.value })} required />
      <button className="btn btn-primary" type="submit">Entrar</button>
    </form>
  );
};

export default Login;
