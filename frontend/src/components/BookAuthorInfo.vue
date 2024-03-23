<template>
    {{ book_details }}

    {{ author_details }}
</template>

<script>
export default{
    name: 'BookAuthorInfo',
    props: ['book_id'],
    data(){
        return {
            error: '',
            book_details: null,
            author_details: null
        }
    },
    methods:{
        async fetchBookByID(){
            try{
                const res = await fetch("http://localhost:8000/api/book/"+this.book_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    }
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data['message']['error'];  // set error
                    this.book_details = null;               // reset output
                }
                else { 
                    this.book_details = data;  // set output
                    this.error = '';           // reset error
                }
            }catch(error){console.log(error);} 
        },
        async fetchAuthorDetails(){
            const author_id = this.book_details['book_details'].a_id;
            try{
                const res = await fetch("http://localhost:8000/api/author/"+author_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    }
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data['message']['error'];  // set error
                    this.author_details = null;               // reset output
                }
                else { 
                    this.author_details = data;  // set output
                    this.error = '';           // reset error
                }
            }catch(error){console.log(error);} 
        }
    },
    async mounted(){
        await this.fetchBookByID();
        if (this.book_details!=null){
            await this.fetchAuthorDetails();
            console.log('complete2')
        }
    }
}
</script>

<style scoped>

</style>