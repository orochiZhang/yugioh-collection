<template>
  <div class="hello">
    <nav class="nav-extended">
      <div class="nav-wrapper">
        
        <ul class="right hide-on-med-and-down">
          <li>
            <input id="content" v-model="content" class="validate">
          </li>  
          <li>
            {{this.content}}
            <a v-on:click="search()" 
              class=" btn-large halfway-fab waves-effect waves-light teal">
              搜索</a>
          </li>
          <li>
            <select v-if="this.loaded == 1" style="display: block" value>
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

    <div class="row" v-if="this.loaded == 1">

      <div class="col s12 m6 l2" v-for="(item, index) in this.datas" :key="item.id">
        <div class="card">
          <div class="card-image">
            <img :src="item.img" />
          </div>
          <div class="card-content">
            <p>{{ item.name }}</p>
          </div>
          <div :class="item.isbuy?'card-action':'card-action blue-grey'">
            <a v-if="!item.isbuy" v-on:click="buy(index)" class="waves-effect waves-light blue btn">标记已有</a>
            <a v-else v-on:click="nobuy(index)" class="waves-effect waves-light btn">取消标记</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Main",
  props: {
    msg: String,
  },
  data(){
    return {
      // this.pagecount = 0
      // this.allcount = 0
      // this.buycount = 0
      // this.rate = 0
      // this.all = 10
      // this.loaded = 0
      // this.datas = []
      // this.content = ""
      pagecount : 0,
      allcount : 0,
      buycount : 0,
      rate : 0,
      all : 10,
      loaded : 0,
      datas : [],
      content : "",
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
            "isbuy": data[index].is_buy,
          }
          l.push(temp)
        }
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$set(this, "pagecount", pagecount)

        console.log(this.datas, this.loaded, this.pagecount)
        this.$forceUpdate();

      }).catch( (error) =>{
          console.log(error);
      });
    },
    setbuy(id) {
      console.log(id);
      this.$axios.get('http://127.0.0.1:5000/buy?id='+id).then((res)=>{
          console.log(res.data);
      }).catch( (error) =>{
          console.log(error);
      })
    },
    setnocard(id) {
      this.$axios.get('http://127.0.0.1:5000/nocard?id='+id).then((res)=>{
          console.log(res.data);
      }).catch( (error) =>{
          console.log(error);
      })
    },
    search() {
      console.log("search", this.content)
      this.$axios.get('http://127.0.0.1:5000/search?content='+this.content+"&isbuy="+this.all).then((res)=>{
        let l = []
        let data = res.data.data
        for (let index in data){
          let temp = {
            'id': index,
            'name': data[index].name,
            'img': "http://127.0.0.1/card/"+index+".jpg",
            "isbuy": data[index].is_buy,
          }
          l.push(temp)
        }
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)
        this.$forceUpdate();
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
      this.getdata(1)
      this.$forceUpdate();
    },
    getcount() {
      this.$axios.get('http://127.0.0.1:5000/count').then((res)=>{
        this.allcount = res.data.all
        this.buycount = res.data.buy
        this.rate = res.data.rate
        this.$forceUpdate();
      }).catch( (error) =>{
          console.log(error);
      })
    }
  }

};
</script>

