<template>
  <div class="hello">
    <div class="row">
      <div class="col s12 m6 l2" v-for="item in items" :key="item.id">
        <div class="card">
          <div class="card-image">
            <img :src="item.img" />
            <span class="card-title">Card Title</span>
          </div>
          <div class="card-content">
            <p>{{ item.name }}</p>
          </div>
          <div class="card-action">
            <input type="checkbox" value="复选框取值" />
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
  data: function () {
    return {
      items: [
        { id: 1, isbuy: 0, name: "Foo", img: "" },
        { id: 2, isbuy: 0, name: "Bar", img: "" },
      ],
    };
  },
};
</script>

