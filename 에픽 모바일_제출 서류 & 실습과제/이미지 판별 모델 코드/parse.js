import Papa from './PapaParse/papaparse';

Papa.parse("https://raw.githubusercontent.com/free-ko/project-js-crawling/main/csv/%EC%BF%A0%ED%8C%A1%EC%A1%B0%ED%9A%8C%EA%B2%B0%EA%B3%BC_%EC%9C%A0%EC%95%84%20%EB%AA%A8%EC%9E%90_2020-12-03.csv", {
	download: true,
	complete: function(results) {
		console.log(results);
	}
});


