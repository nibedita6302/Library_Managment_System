<template>
    <!-- Modal -->
    <div class="modal fade" id="info6" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">{{ message }}</p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>

    <div class="container p-5">
        <form @submit.prevent="selectAPI">
            <legend>Book {{ book_id? "Update":"Create" }} Form:</legend>
            <div class="mb-3" v-for="f in form_fields" :key="f.id">
                <td>
                    <label :for="f.id">{{ f.label }}:</label>
                </td>
                <td>
                    <input v-if="f.type=='file'" :type="f.type" :id="f.id" accept="image/*" v-model="f.data">
                    <input v-else-if="f.type=='number'" :type="f.type" :id="f.id" :min="f.min" :step="f.step" 
                    :placeholder="placeholder(f.id)" v-model="f.data"/>
                    <select v-else-if="f.type=='select' && f.id=='a_id'" :id="f.id"  v-model="f.data" >
                        <option v-for="a in author_data" name="{{a.a_id}}" :value="a.a_id" :key="a.a_id">
                            {{ a.a_name }}
                        </option>
                    </select>
                    <select v-else-if="f.type=='select' && f.id=='s_id'" :id="f.id"  v-model="f.data" >
                        <option v-for="s in section_data" name="{{s.s_id}}" :value="s.s_id" :key="s.s_id">
                            {{ s.s_name }}
                        </option>
                    </select>
                    <input v-else :type="f.type" :id="f.id" :placeholder="placeholder(f.id)" v-model="f.data" />
                </td>
            </div>
            <button class="btn btn-primary" type="submit" data-bs-toggle="modal" data-bs-target="#info6">
                Submit
            </button>
        </form>
    </div>
</template>

<script>
export default{
    name: 'BookForm',
    data(){
        return{
            book_id: this.$route.params.book_id,
            token: localStorage.getItem('auth_token'),
            book_data: {},
            author_data: [],
            section_data: [],
            message: '',
            form_fields: [
                {label: 'Book Name', type:'text', id:'b_name', data:''},
                {label: 'Book Summary', type:'text', id:'summary', data:''},
                {label: 'Book Image', type:'file', id:'b_image'},
                {label: 'Select Author', type:'select', id:'a_id', data:''},
                {label: 'Select Section', type:'select', id:'s_id', data:''},
                {label: 'PDF Price', type:'number', min:"1", step:"0.01", id:'pdf_price', data:''},
                {label: 'Publisher', type:'text', id:'publisher', data:''},
                {label: 'Published Date', type:'date', id:'date_published', data:''},
                {label: 'Content ID (Only View)', type:'text', id:'content_view_id', data:''},
                {label: 'Content ID (Download)', type:'text', id:'content_download_id', data:''}
            ],
        }
    },
    methods:{
        placeholder(atr){
            return this.book_id? this.book_data[atr]: ''
        },
        selectAPI(){
            var newData = new FormData()
            const image = document.getElementById('s_image')
            if (image && image.files.length>0) {
                newData.append("s_image",image.files[0]);
            }
            for(let f in this.form_fields){
                if (this.form_fields[f].data!=''){
                    if (this.form_fields[f].type=='date'){
                        // Format date in DD/MM/YYYY
                        const date = new Date(this.form_fields[f].data)
                        const formatDate = `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`
                        newData.append(this.form_fields[f].id,formatDate);
                    }
                    else if (this.form_fields[f].type!=='file') {
                        newData.append(this.form_fields[f].id,this.form_fields[f].data);
                    }
                }
            }
            // for (var p of newData.entries()){console.log(p[0],p[1])}
            if (this.book_id==null){this.createBook(newData);}
            else {this.updateBook(newData)}
        },
        async updateBook(newData){
            try{
                const res = await fetch('http://localhost:8000/api/book/update/'+this.book_id, {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    },
                    body: newData
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Book Update:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        },
        async createBook(newData){
            try{
                const res = await fetch('http://localhost:8000/api/book/create', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    },
                    body: newData
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Book Update:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        },
        async fetchBookByID(){
            try{
                const res = await fetch('http://localhost:8000/api/book/'+this.book_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at fetch Book by ID:"+res.status) }
                const data = await res.json() ;
                this.book_data = data.book_details;  // set output
            }catch(error){console.log(error);} 
        },
        async fetchAuthorByID(){
            try{
                const res = await fetch('http://localhost:8000/api/all-authors', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at fetch Book by ID:"+res.status) }
                const data = await res.json() ;
                this.author_data = data;  // set output
            }catch(error){console.log(error);} 
        },
        async fetchSectionByID(){
            try{
                const res = await fetch('http://localhost:8000/api/home/sections', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at fetch Book by ID:"+res.status) }
                const data = await res.json() ;
                this.section_data = data;  // set output
            }catch(error){console.log(error);} 
        },
    },
    created(){
        if (this.book_id!=null){ 
            this.fetchBookByID(); 
            this.fetchAuthorByID();
            this.fetchSectionByID();
        }
    }
}
</script>

<style scoped>
form{
    text-align: left;
    padding: 40px;
}
td{
    width: 200px;
}
</style>