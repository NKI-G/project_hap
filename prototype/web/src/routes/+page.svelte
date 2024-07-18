<script>
    import { onMount } from "svelte";
    var url = 'http://localhost:8000';
    let rsss;

    // 접속 국가 확인
    let lang = navigator.language
    console.log(lang)

    onMount(async () => {
        fetch(`${url}/add?gold=100&country=${lang}`, {method: "POST",})
    .then((data) => {return data.json()})
    .then((res) => {console.log(res);rsss=JSON.stringify(res)})  
        fetch(url)
    .then((data) => {return data.json()})
    .then((res) => {console.log(res);rsss=JSON.stringify(res)})
    })
    
</script>

<h3>현제 접속국가는 {lang}입니다. 바꾸시고 싶으시면 브라우저 언어를 바꿔주세요.</h3>
<p>{rsss}</p>