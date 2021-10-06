<template>
  <div class="hello">
    <nav class="nav-extended">
      <div class="nav-wrapper">
        <ul class="left hide-on-med-and-down">
          <li>
            <router-link to="/">Go to 全卡浏览</router-link>
          </li>
        </ul>
        <ul class="right hide-on-med-and-down">  
          <li style="margin-right: 10px;">
            <select v-if="this.loaded == 1" style="display: block; margin-top: 10px;" value>
              <option 
                v-for="series in this.series_list" :key="series" :value="series" v-on:click="setseries(series)" >
                {{series}}
              </option>
            </select>
          </li>
          <li>
            <select v-if="this.loaded == 1" style="display: block; margin-top: 10px;" value>
              <option 
                v-for="pack in this.pack_dict[this.series]" :key="pack" 
                :value="pack" v-on:click="setpack(pack)">
                {{pack}}
              </option>
            </select>
          </li>
          <li>
            <a v-on:click="setallbuy()" class=" btn-large halfway-fab waves-effect waves-light teal">
                一键标记</a>
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
          <div class="card-content" style="height: 80px;">
            <p>{{ item.name }}</p>
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
  name: "Pack",
  data(){
    return {
      loaded : 0,
      pack_dict : {},
      series_list : [],
      pack : "",
      series : "",
      datas : [],
      content : "",
    }

  },
  mounted(){
    this.getpacklist()
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
    getpacklist() {
      this.$axios.get('http://127.0.0.1:5000/pack_list').then((res)=>{
        let series_list = []
        let pack_dict = {}
        pack_dict = res.data
        console.log(this.pack_dict, res.data);
        for (let series in res.data){
          series_list.push(series)
        }
        
        this.$set(this, "pack_dict", pack_dict)
        this.$set(this, "series_list", series_list)
        this.$set(this, "series", series_list[0])
        this.$set(this, "pack", pack_dict[this.series][0])
        this.$set(this, "loaded", 1)
        this.getdata()
        this.$forceUpdate();
        
      }).catch( (error) =>{
          console.log(error);
      });
    },
    setseries(series) {
        this.$set(this, "series", series)
        this.$set(this, "pack", this.pack_dict[this.series][0])
        this.getdata()
    },
    setpack(pack) {
        this.$set(this, "pack", pack)
        this.getdata()
    },
    getdata() {
      this.$axios.get('http://127.0.0.1:5000/pack_info?series='+this.series+'&pack='+this.pack,).then((res)=>{
        let data = res.data
        let l =[]
        for (let index in data){
          let i = data[index].name ? index : 0
          let temp = {
            'id': index,
            'name': data[index].name ? data[index].name : data[index].card_no,
            'img': "http://127.0.0.1/card/"+i+".jpg",
            "isbuy": data[index].isbuy,
          }
          l.push(temp)
        }
        console.log(data);  
        this.$set(this, "datas", l)
        this.$set(this, "loaded", 1)

        console.log(this.datas)
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
  }

};
</script>

