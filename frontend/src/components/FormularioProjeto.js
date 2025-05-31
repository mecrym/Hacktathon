import React, { useState } from 'react';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';
import salvarJson from '../utils/salvarJson';

const FormularioProjeto = () => {
  const [form, setForm] = useState({
    nome: '',
    largura: '',
    comprimento: '',
    frontal: '',
    laterais: '',
    fundos: '',
    descricao: '',
    comodos: '',
  });

  const [sucesso, setSucesso] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const jsonData = {
      metadata: { nome: form.nome },
      lote: {
        largura: parseFloat(form.largura),
        comprimento: parseFloat(form.comprimento),
        restricoes: {
          recuos: {
            frontal: parseFloat(form.frontal),
            laterais: parseFloat(form.laterais),
            fundos: parseFloat(form.fundos),
          },
        },
      },
      descricao_usuario: form.descricao,
      comodos: form.comodos.split(',').map((item) => {
        const [tipo, quantidade] = item.trim().split(':');
        return { tipo, quantidade: parseInt(quantidade) };
      }),
    };

    salvarJson(jsonData);
    setSucesso(true);
  };

  return (
    <Container>
      <h2 className="my-4">Projeto Residencial</h2>
      {sucesso && <Alert variant="success">Dados salvos com sucesso!</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Nome do Projeto</Form.Label>
          <Form.Control name="nome" onChange={handleChange} />
        </Form.Group>

        <Row>
          <Col><Form.Label>Largura (m)</Form.Label><Form.Control name="largura" onChange={handleChange} /></Col>
          <Col><Form.Label>Comprimento (m)</Form.Label><Form.Control name="comprimento" onChange={handleChange} /></Col>
        </Row>

        <Row className="mt-3">
          <Col><Form.Label>Recuo Frontal</Form.Label><Form.Control name="frontal" onChange={handleChange} /></Col>
          <Col><Form.Label>Recuo Lateral</Form.Label><Form.Control name="laterais" onChange={handleChange} /></Col>
          <Col><Form.Label>Recuo Fundos</Form.Label><Form.Control name="fundos" onChange={handleChange} /></Col>
        </Row>

        <Form.Group className="mt-3">
          <Form.Label>Descrição do Usuário</Form.Label>
          <Form.Control name="descricao" as="textarea" rows={3} onChange={handleChange} />
        </Form.Group>

        <Form.Group className="mt-3">
          <Form.Label>Cômodos (ex: quarto:2, sala:1, banheiro:2)</Form.Label>
          <Form.Control name="comodos" onChange={handleChange} />
        </Form.Group>

        <Button className="mt-3" variant="primary" type="submit">Salvar</Button>
      </Form>
    </Container>
  );
};

export default FormularioProjeto;
