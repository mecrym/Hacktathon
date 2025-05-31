import { useState } from 'react';

const Cadastro = ({ setMensagem }) => {
  const [cadastro, setCadastro] = useState({
    nome: '', email: '', telefone: '', tipo: 'comum',
    cpf: '', crea: '', senha: '', confirmarSenha: ''
  });

  const usuarios = JSON.parse(localStorage.getItem('data.json')) || [];

  const salvarUsuarios = (dados) => {
    localStorage.setItem('data.json', JSON.stringify(dados));
  };

  const handleCadastro = (e) => {
    e.preventDefault();
    if (cadastro.senha !== cadastro.confirmarSenha) {
      setMensagem('As senhas não coincidem');
      return;
    }

    const existe = usuarios.find(u => u.email === cadastro.email);
    if (existe) {
      setMensagem('Usuário já cadastrado');
      return;
    }

    const novoUsuario = {
      nome: cadastro.nome,
      email: cadastro.email,
      telefone: cadastro.telefone,
      tipo: cadastro.tipo,
      identificador: cadastro.tipo === 'comum' ? cadastro.cpf : cadastro.crea,
      senha: cadastro.senha
    };

    salvarUsuarios([...usuarios, novoUsuario]);
    setMensagem('Cadastro realizado com sucesso!');

    setCadastro({
      nome: '', email: '', telefone: '', tipo: 'comum',
      cpf: '', crea: '', senha: '', confirmarSenha: ''
    });
  };

  return (
    <form onSubmit={handleCadastro} className="w-50 mx-auto mt-4">
      <h2>Cadastro</h2>
      <input className="form-control mb-2" type="text" placeholder="Nome" value={cadastro.nome} onChange={e => setCadastro({ ...cadastro, nome: e.target.value })} required />
      <input className="form-control mb-2" type="email" placeholder="Email" value={cadastro.email} onChange={e => setCadastro({ ...cadastro, email: e.target.value })} required />
      <input className="form-control mb-2" type="tel" placeholder="Telefone" value={cadastro.telefone} onChange={e => setCadastro({ ...cadastro, telefone: e.target.value })} required />
      <select className="form-control mb-2" value={cadastro.tipo} onChange={e => setCadastro({ ...cadastro, tipo: e.target.value })}>
        <option value="comum">Comum</option>
        <option value="engenheiro">Engenheiro</option>
      </select>
      {cadastro.tipo === 'comum' ? (
        <input className="form-control mb-2" type="text" placeholder="CPF" value={cadastro.cpf} onChange={e => setCadastro({ ...cadastro, cpf: e.target.value })} required />
      ) : (
        <input className="form-control mb-2" type="text" placeholder="CREA" value={cadastro.crea} onChange={e => setCadastro({ ...cadastro, crea: e.target.value })} required />
      )}
      <input className="form-control mb-2" type="password" placeholder="Senha" value={cadastro.senha} onChange={e => setCadastro({ ...cadastro, senha: e.target.value })} required />
      <input className="form-control mb-2" type="password" placeholder="Confirmar senha" value={cadastro.confirmarSenha} onChange={e => setCadastro({ ...cadastro, confirmarSenha: e.target.value })} required />
      <button className="btn btn-success" type="submit">Cadastrar</button>
    </form>
  );
};

export default Cadastro;
