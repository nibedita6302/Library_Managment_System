<template>
    <!-- Modal -->
    <div class="modal fade" id="info3" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
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
            <legend>Section {{ section_id? "Update":"Create" }} Form:</legend>
            <div class="mb-3">
                <label for="s_name" class="form-label">Section Name</label>
                <input type="text" class="form-control" id="s_name" aria-describedby="help"
                :placeholder="section_id? section_data.s_name:''">
                <div id="help" class="form-text">Section name must be unique</div>
            </div>
            <div class="mb-3">
                <label for="s_image">Section Image</label>
                <input type="file" accept="image/*" class="form-control" id="s_image" >
                <div id="help" class="form-text">{{ section_id? section_data.s_image:'' }}</div>
            </div>
            <button type="submit" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#info3">
                Submit
            </button>
        </form>
    </div>
</template>

<script>
export default{
    name: 'SectionForm',
    data(){
        return{
            section_id: this.$route.params.section_id,
            token: localStorage.getItem('auth_token'),
            section_data: {},
            message: ''
        }
    },
    methods:{
        async fetchSectionByID(){
            try{
                const res = await fetch('http://localhost:8000/api/section/'+this.section_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at fetch Section by ID:"+res.status) }
                const data = await res.json() ;
                this.section_data = data;  // set output
            }catch(error){console.log(error);} 
        },
        selectAPI(){
            var newData = new FormData()
            const image = document.getElementById('s_image')
            const name = document.getElementById('s_name')
            if (image && image.files.length>0) {
                newData.append("s_image",image.files[0]);
            }
            newData.append("s_name", name.value)
            if (this.section_id==null){this.createSection(newData);}
            else {this.updateSection(newData)}
        },
        async updateSection(newData){
            try{
                const res = await fetch('http://localhost:8000/api/section/update/'+this.section_id, {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    },
                    body: newData
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Section Update:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        },
        async createSection(newData){
            try{
                const res = await fetch('http://localhost:8000/api/section/create', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    },
                    body: newData
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Section Update:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        }
    },
    created(){
        if (this.section_id!=null){ this.fetchSectionByID(); }
    }
}
</script>

<style scoped>
form{
    text-align: left;
    padding: 40px;
}
</style>