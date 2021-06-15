<template>
    <div class='page-not-found'>
        <div class='pnf-img'></div>
        <p class=''>Pagina niet gevonden</p>
    </div>
</template>

<style scoped>
    .page-not-found{
        width: 100%;
        height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #f5f5dc;
    }
    .pnf-img{
        width: 200px;
        height: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('../assets/error.png');
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }
    .page-not-found p{
        font-size: 25px;
        text-align: center;
        font-weight: bold;
    }
</style>