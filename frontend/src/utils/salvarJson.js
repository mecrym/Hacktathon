const salvarJson = async (dados) => {
  try {
    const resposta = await fetch("http://localhost:5000/salvar-json", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    if (!resposta.ok) throw new Error("Erro ao salvar JSON");

    const resultado = await resposta.json();
    console.log("✅ JSON salvo:", resultado);
  } catch (erro) {
    console.error("❌ Falha ao enviar JSON:", erro);
    alert("Erro ao enviar dados. Veja o console.");
  }
};

export default salvarJson;
