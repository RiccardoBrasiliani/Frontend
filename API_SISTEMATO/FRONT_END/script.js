document.addEventListener('DOMContentLoaded', () => {
    generaRigheProdotti(); // Chiamata per generare le righe dei prodotti al caricamento della pagina
});

const HOST = "http://localhost:8888";

function generaRigheProdotti() {
    fetch(`${HOST}/products`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta');
            }
            return response.json();
        })
        .then(response => {
            $('#tbody-prodotti').empty(); // Svuota il tbody prima di aggiungere le righe

            if (response.hasOwnProperty('data')) {
                response.data.forEach(record => {
                    aggiungiRigaProdotto(record); // Aggiungi riga per ogni prodotto
                });
            } else {
                console.error("Errore: La risposta non contiene il campo 'data'.");
            }
        })
        .catch(error => {
            console.error("Errore nella richiesta fetch:", error);
        });
}

function aggiungiRigaProdotto(record) {
    const riga = `
        <tr id="prodotto-${record.id}">
            <td>${record.id}</td>
            <td>${record.attributes.nome}</td>
            <td>${record.attributes.marca}</td>
            <td>${record.attributes.prezzo}</td>
            <td>
                <button onclick="modificaProdotto(${record.id})" class="btn btn-primary">Modifica</button>
                <button onclick="eliminaProdotto(${record.id})" class="btn btn-danger">Elimina</button>
                <button onclick="mostraDettagli(${record.id})" class="btn btn-info">Mostra Dettagli</button>
            </td>
        </tr>
    `;
    $('#tbody-prodotti').append(riga);
}

function modificaProdotto(id) {
    fetch(`${HOST}/products/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta');
            }
            return response.json();
        })
        .then(data => {
            // Verifica che la risposta contenga l'oggetto 'data' con gli attributi necessari
            if (data && data.data && data.data.attributes) {
                // Assegna i valori ricevuti ai campi del form nel modale
                $('#modifica-id').val(id);
                $('#modifica-nome').val(data.data.attributes.nome);
                $('#modifica-marca').val(data.data.attributes.marca);
                $('#modifica-prezzo').val(data.data.attributes.prezzo);

                // Apri il modale di modifica
                $('#modificaModal').modal('show');
            } else {
                console.error("Errore: Dati mancanti nella risposta.");
            }
        })
        .catch(error => {
            console.error("Errore nella richiesta fetch:", error);
        });
}

function eliminaProdotto(id) {
    $('#confermaEliminazioneModal').modal('show');
    idProdottoDaEliminare = id;
}

function confermaEliminazione() {
    $('#confermaEliminazioneModal').modal('hide');
    eliminaProdottoDallaTabella(idProdottoDaEliminare);
    eliminaProdottoDalDatabase(idProdottoDaEliminare);
}

let idProdottoDaEliminare;

function eliminaProdottoDallaTabella(id) {
    $(`#prodotto-${id}`).remove(); // Rimuovi la riga dalla tabella utilizzando l'ID univoco
}

function eliminaProdottoDalDatabase(id) {
    fetch(`${HOST}/products/${id}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Errore nella richiesta');
        }
        console.log("Prodotto eliminato con successo dal database");
    })
    .catch(error => {
        console.error("Errore nella richiesta fetch:", error);
    });
}

function salvaModifiche() {
    var id = $('#modifica-id').val();
    var nome = $('#modifica-nome').val();
    var marca = $('#modifica-marca').val();
    var prezzo = $('#modifica-prezzo').val();

    var nuovoProdotto = {
        data: {
            type: 'products',
            id: id,
            attributes: {
                nome: nome,
                marca: marca,
                prezzo: prezzo
            }
        }
    };

    fetch(`${HOST}/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(nuovoProdotto),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Errore nella richiesta');
        }
        console.log("Prodotto aggiornato con successo nel database");
        aggiornaRigaNellaTabella(id, nuovoProdotto);
        $('#modificaModal').modal('hide');
    })
    .catch(error => {
        console.error("Errore nella richiesta fetch:", error);
    });
}

function aggiornaRigaNellaTabella(id, nuovoProdotto) {
    var rigaProdotto = $(`#prodotto-${id}`);
    rigaProdotto.find('td:nth-child(2)').text(nuovoProdotto.data.attributes.nome);
    rigaProdotto.find('td:nth-child(4)').text(nuovoProdotto.data.attributes.prezzo);
    rigaProdotto.find('td:nth-child(3)').text(nuovoProdotto.data.attributes.marca);
}
function mostraDettagli(id) {
    fetch(`${HOST}/products/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta');
            }
            return response.json();
        })
        .then(data => {
            $('#dettagli-nome').text(data.data.attributes.nome);
            $('#dettagli-marca').text(data.data.attributes.marca);
            $('#dettagli-prezzo').text(data.data.attributes.prezzo);

            $('#dettagliProdottoModal').modal('show');
        })
        .catch(error => {
            console.error("Errore nella richiesta fetch:", error);
        });
}

function mostraModaleCreaProdotto() {
    $('#nome').val('');
    $('#marca').val('');
    $('#prezzo').val('');

    $('#creaProdottoModal').modal('show');
}

function salvaNuovoProdotto() {
    var nome = $('#nome').val();
    var marca = $('#marca').val();
    var prezzo = $('#prezzo').val();

    var nuovoProdotto = {
        data: {
            attributes: {
                nome: nome,
                marca: marca,
                prezzo: prezzo
            }
        }
    };

    fetch(`${HOST}/products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(nuovoProdotto),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Errore nella richiesta');
        }
        console.log("Nuovo prodotto inserito con successo nel database");
        $('#creaProdottoModal').modal('hide');
        generaRigheProdotti(); // Aggiorna la tabella dopo l'inserimento
    })
    .catch(error => {
        console.error("Errore nella richiesta fetch:", error);
    });
}