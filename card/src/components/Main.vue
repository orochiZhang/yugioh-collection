<template>
  <div class="hello">
    <nav class="nav-extended">
      <div class="nav-wrapper">
        <ul class="left hide-on-med-and-down">
          <li>
            <router-link to="pack">Go to 按卡包查询</router-link>
          </li>
        </ul>
        <ul class="right hide-on-med-and-down">

          <li style="margin-right: 10px;">
            <select v-if="this.loaded == 1" style="display: block; margin-top: 10px;">
              <option :key="1" :value="1" v-on:click="changesearchtype(1)">卡名，效果，卡密</option>
              <option :key="2" :value="2" v-on:click="changesearchtype(2)">卡名</option>
              <option :key="3" :value="3" v-on:click="changesearchtype(3)">卡片编号</option>
            </select>
           <li>
          <li>
            <input id="content" v-model="content" class="validate">
          </li>  
          <li>
            <a v-on:click="search()" 
              class=" btn-large halfway-fab waves-effect waves-light teal">
              搜索</a>
          </li>
          <li>
            <a v-if="this.search_flag == 1" v-on:click="getdata(1)" 
              class=" btn-large halfway-fab waves-effect waves-light teal">
              取消搜索</a>
          </li>
          <li>
            <select v-if="this.loaded == 1 && this.search_flag == 0" style="display: block; margin-top: 10px;">
              <option 
                v-for="count in this.pagecount" :key="count" 
                :value="count" v-on:click="getdata(count)">
                page {{count}}
              </option>
            </select>
          </li>
          <li><a>已有/总数：{{this.buycount}}/{{this.allcount}}</a></li>
          <li><a>收集进度：{{this.rate}} %</a></li>
          <li>
          <a v-on:click="allOrOnlyNo()" 
          class=" btn-large halfway-fab waves-effect waves-light teal">
            {{this.all?"全部卡":"仅没买的"}}</a>
        </li>
        </ul>
      </div>
    </nav>

    <div class="chip chips-initial" style="margin:10px">本页一共有{{this.datas.length}}张数据</div>
    <div class="chip chips-initial" style="margin:10px">本页收集率：{{this.page_rate}}%</div>
    <a v-if="this.search_flag == 1" v-on:click="setallbuy()" class=" btn-small halfway-fab waves-effect waves-light teal">
      一键标记
    </a>

    <div class="row" v-if="this.loaded == 1">
      <div class="col s12 m6 l2" v-for="(item, index) in this.datas" :key="item.id">
        <div class="card">
          <div class="card-image">
            <img :src="item.img" />
          </div>
          <div class="card-content" style="height: 80px;">
            <p>{{ item.name }}</p>
             <p v-if="'atk' in item">ATK: {{item.atk}} </p>
          </div>
          <div :class="item.isbuy?'card-action':'card-action blue-grey'">
            <a v-if="!item.isbuy" v-on:click="buy(index)" class="waves-effect waves-light blue btn">标记已有</a>
            <a v-else v-on:click="nobuy(index)" class="waves-effect waves-light btn">✔，取消标记</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Main",
  data(){
    return {
      pagecount : 0,
      allcount : 0,
      buycount : 0,
      rate : 0,
      all : 10,
      loaded : 0,
      datas : [],
      content : "",
      search_flag: 0,
      searchtype: 1,
      page_rate: 0,
    }

  },
  mounted(){
    this.getdata(1)
    this.getcount()
  },
  methods:{
    buy(index) {
      this.datas[index].isbuy = 1
      this.$forceUpdate();
      this.setbuy(this.datas[index].id)
    },
    nobuy(index) {
      this.datas[index].isbuy = 0
      this.$forceUpdate();
      this.setnocard(this.datas[index].id)
    },
    getdata(page) {
      this.$axios.get('http://127.0.0.1:5000/?page='+page+'&isbuy='+this.all,).then((res)=>{
        let l = []
        let data = res.data.data
        let pagecount = res.data.page_all
        for (let index in data){
          let temp = {
            'id': index,
            'name': data[index].name,
            'img': "http://127.0.0.1/card/"+index+".jpg",
            "isbuy": data[index].isbuy,
          }
          l.push(temp)
        }
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$set(this, "pagecount", pagecount)
        this.$set(this, "search_flag", 0)

        this.getcount();
        this.$forceUpdate();

      }).catch( (error) =>{
          console.log(error);
      });
    },
    setallbuy() {
      for (var i=0;i<this.datas.length;i++){ 
          this.buy(i)
      }
    },
    setbuy(id) {
      if (id == 0) {
        return
      }
      this.$axios.get('http://127.0.0.1:5000/buy?id='+id).then((res)=>{
          console.log(res.data);
          this.getcount()
      }).catch( (error) =>{
          console.log(error);
      })
    },
    setnocard(id) {
      this.$axios.get('http://127.0.0.1:5000/nocard?id='+id).then((res)=>{
          console.log(res.data);
          this.getcount()
      }).catch( (error) =>{
          console.log(error);
      })
    },
    changesearchtype(searchtype) {
      this.$set(this, "searchtype", searchtype)
    },
    search() {
      if (this.searchtype == 1){
        this.search_all()
      }else if (this.searchtype == 2){
        this.search_name()
      }else if (this.searchtype == 3){
        this.search_pack_number()
      }
    },
    search_all() {
      this.$axios.get('http://127.0.0.1:5000/search?content='+this.content+"&isbuy="+this.all).then((res)=>{
        let l = []
        let data = res.data.data
        for (let index in data){
          let temp = {
            'id': index,
            'name': data[index].name,
            'img': "http://127.0.0.1/card/"+index+".jpg",
            "isbuy": data[index].isbuy,
            "atk": Number(data[index].atk),
          }
          l.push(temp)
        }
        l = l.sort(function(a,b){return a.atk > b.atk})
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$set(this, "search_flag", 1)
        this.$forceUpdate()
        this.getcount()
      }).catch( (error) =>{
          console.log(error);
      })
    },
    search_name() {
      this.$axios.get('http://127.0.0.1:5000/search/name?content='+this.content+"&isbuy="+this.all).then((res)=>{
        let l = []
        let data = res.data.data
        for (let index in data){
          let temp = {
            'id': index,
            'name': data[index].name,
            'img': "http://127.0.0.1/card/"+index+".jpg",
            "isbuy": data[index].isbuy,
          }
          l.push(temp)
        }
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$set(this, "search_flag", 1)
        this.$forceUpdate()
        this.getcount()
      }).catch( (error) =>{
          console.log(error);
      })
    },
    search_pack_number() {
      this.$axios.get('http://127.0.0.1:5000/search/packnumber?content='+this.content+"&isbuy="+this.all).then((res)=>{
        let l = []
        let img_url = '0'
        let data = res.data.data
        for (let index in data){
          if (index < 0){
            img_url = '0'
          }else{
            img_url = index
          }
            
          let temp = {
            'id': index,
            'name': data[index].name,
            'img': "http://127.0.0.1/card/"+img_url+".jpg",
            "isbuy": data[index].isbuy,
          }
          l.push(temp)
        }
        l = l.sort(function(a,b){return a.name.localeCompare(b.name)})
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$set(this, "search_flag", 1)
        this.$forceUpdate()
        this.getcount()
      }).catch( (error) =>{
          console.log(error);
      })
    },
    allOrOnlyNo() {
      if (this.all == 10) {
        this.$set(this, "all", 0)
      }else{
        this.$set(this, "all", 10)
      }
      if (this.search_flag == 0) {
        this.getdata(1)
      }else {
        this.search()
      }
      
      this.$forceUpdate();
    },
    getcount() {
      this.$axios.get('http://127.0.0.1:5000/count').then((res)=>{
        this.allcount = res.data.all
        this.buycount = res.data.buy
        this.rate = res.data.rate
        let all = 0
        let buy = 0
        for (let index in this.datas){
          all += 1
          if (this.datas[index].isbuy == 1){
            buy += 1
          }
        }
        if (all == 0){
          this.page_rate = 0
        }else{
          this.page_rate = (buy / all * 100).toFixed(2)
        }
        this.$forceUpdate();
      }).catch( (error) =>{
          console.log(error);
      })
    }
  }

};
</script>

