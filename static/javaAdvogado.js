document.getElementById('formulario').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    console.log('Enviando dados:', Object.fromEntries(formData));

    try {
        const response = await fetch('/cadastro/advogado', {
            method: 'POST',
            body: formData
        });

        console.log('Resposta do servidor:', response.status, response.statusText);

        if (response.redirected) {
            alert('Advogado cadastrado com sucesso!');
            this.reset();
            window.location.href = response.url; // Segue o redirecionamento
            return;
        }

        if (!response.ok) {
            const data = await response.json();
            console.log('Dados recebidos:', data);
            if (response.status === 409) {
                alert('Erro: Este email já está cadastrado!');
            } else {
                alert('Erro: ' + (data.message || 'Falha ao cadastrar. Tente novamente.'));
            }
            return;
        }

        // Caso a resposta seja ok mas não redirecione (fallback)
        alert('Usuário cadastrado com sucesso!');
        this.reset();

    } catch (error) {
        console.error('Erro ao conectar com o servidor:', error);
        alert('Erro ao conectar com o servidor. Verifique sua conexão ou tente novamente.');
    }
});