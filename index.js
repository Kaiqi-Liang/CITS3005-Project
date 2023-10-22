const SERVER_URL = 'http://127.0.0.1:5000/'
const form = document.forms.form;
form.query.addEventListener("change", function() { 
	form.input1.value = '';
	form.input2.value = '';
	form.input1.placeholder = '';
	form.input2.placeholder = '';
	form.input1.style.display = 'none';
	form.input2.style.display = 'none';
	form.assessment.style.display = 'none';
	form.contact_hour.style.display = 'none';
    switch (this.value) {
		case 'query1':
			form.input1.type = 'number';
			form.input1.placeholder = 'number of outcomes';
			form.input1.style.display = 'inline-block';
			break;
		case 'query2':
			form.input1.type = 'number';
			form.input1.placeholder = 'unit level';
			form.input1.style.display = 'inline-block';
			break;
		case 'query3':
			form.input1.type = 'number';
			form.input1.placeholder = 'number of majors';
			form.input1.style.display = 'inline-block';
			break;
		case 'query4':
			form.input1.type = 'text';
			form.input1.placeholder = 'search term';
			form.input1.style.display = 'inline-block';
			break;
		case 'query5':
			form.input1.type = 'text';
			form.input1.placeholder = 'my major code';
			form.input1.style.display = 'inline-block';
			form.input2.type = 'text';
			form.input2.placeholder = 'unit code';
			form.input2.style.display = 'inline-block';
			break;
		case 'query6':
			form.input1.type = 'number';
			form.input1.placeholder = 'number of hours';
			form.input1.style.display = 'inline-block';
			form.contact_hour.style.display = 'inline-block';
			break;
		case 'query7':
			form.assessment.style.display = 'inline-block';
			break;
		case 'query8':
			form.input1.type = 'text';
			form.input1.placeholder = 'my major code';
			form.input1.style.display = 'inline-block';
			form.input2.type = 'number';
			form.input2.placeholder = 'number of units';
			form.input2.style.display = 'inline-block';
			break;
		case 'other':
			form.input1.type = 'text';
			form.input1.placeholder = 'sparql query';
			form.input1.style.display = 'inline-block';
			break;
		default:
			break;
	}
});

form.addEventListener('submit', async (event) => {
	form.querySelector('input[type=submit]').disabled = true;
	event.preventDefault();
	document.querySelector('img').style.display = 'block';
	document.body.removeChild(document.body.lastChild);
	const payload = {};
    switch (form.query.value) {
		case 'query1':
			payload.outcomes = form.input1.value;
			break;
		case 'query2':
			payload.level = form.input1.value;
			break;
		case 'query3':
			payload.majors = form.input1.value;
			break;
		case 'query4':
			payload.query = form.input1.value;
			break;
		case 'query5':
			payload.major_code = form.input1.value;
			payload.unit_code = form.input2.value;
			break;
		case 'query6':
			payload.hours = form.input1.value;
			payload.contact_hour = form.contact_hour.value;
			break;
		case 'query7':
			payload.assessment = form.assessment.value;
			break;
		case 'query8':
			payload.major_code = form.input1.value;
			payload.units = form.input2.value;
			break;
		case 'shacl':
			const res = await fetch(`${SERVER_URL}shacl`);
			const data = await res.text();
			const pre = document.createElement('pre');
			pre.textContent = data;
			document.body.appendChild(pre);
			form.querySelector('input[type=submit]').disabled = false;
			document.querySelector('img').style.display = 'none';
			return;
		case 'other':
			payload.query = form.input1.value.trim();
		default:
			break;
	}
	try {
		const res = await fetch(`${SERVER_URL}${form.query.value}`, {
			method: 'post',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify(payload),
		});
		const data = await res.json();
		const ul = document.createElement('ul');
		document.body.appendChild(ul);
		if (data.length === 0) {
			const p = document.createElement('p');
			p.textContent = 'No matching result for the query';
			document.body.appendChild(p);
		} else {
			for (const value of data) {
				const li = document.createElement('li');
				for (const atom of value) {
					if (atom.includes('=')) {
						const a = document.createElement('a');
						a.href = value;
						a.target = '_blank';
						a.textContent = atom.split('=')[1];
						li.appendChild(a);
					} else {
						const span = document.createElement('span');
						span.style.marginLeft = '10px';
						span.textContent = atom;
						li.appendChild(span);
					}
				}
				ul.appendChild(li);
			}
		}
	} catch (error) {
		console.warn(error);	
		const p = document.createElement('p');
		p.textContent = 'Something went wrong';
		document.body.appendChild(p);
	}
	form.querySelector('input[type=submit]').disabled = false;
	document.querySelector('img').style.display = 'none';
});
