<template>
  <div>
    <!-- 用户喜欢的文章列表 -->
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> Liked Blogs <small v-if="blogs">(共 {{ blogs._meta.total_items }} 篇, {{ blogs._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>
            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="blogs" class="card-block g-pa-0" >

        <div class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20"
          v-for="(blog, index) in blogs.items" v-bind:key="index">
          
          <router-link v-bind:to="{ path: `/user/${blog.author.id}` }" v-bind:title="blog.author.name || blog.author.username">
            <span v-if="blog.is_new" class="d-inline-block g-pos-rel">
              <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
              <img class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="blog.author.avatar" v-bind:alt="blog.author.name || blog.author.username">
            </span>
            <img v-else class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="blog.author.avatar" v-bind:alt="blog.author.name || blog.author.username">
          </router-link>
          
          <div class="media-body">
            <div class="g-mb-15">
              <h5 class="h5 g-color-gray-dark-v1 mb-0">
                <small class="g-font-size-12 g-color-aqua g-mr-5">你喜欢了</small>
                <router-link v-bind:to="{ path: `/user/${blog.author.id}` }" class="g-text-underline--none--hover">{{ blog.author.name || blog.author.username }}</router-link>
                <span class="h6 g-color-aqua">的文章<router-link v-bind:to="{ name: 'BlogDetail', params: { id: blog.id } }" class="g-text-underline--none--hover">《{{ blog.title }}》</router-link></span>
              </h5>
              <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(blog.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
            </div>

            <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
            v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
            <vue-markdown
              :source="blog.summary"
              class="markdown-body g-mb-15"
              v-highlight>
            </vue-markdown>

            <div class="d-flex justify-content-start">
              <ul class="list-inline mb-0">
                <li class="list-inline-item g-mr-20">
                  <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
                    <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ blog.views }}
                  </a>
                </li>
                <li class="list-inline-item g-mr-20">
                  <router-link v-bind:to="{ path: `/blog/${blog.id}#like-blog` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
                    <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ blog.likers_count }}
                  </router-link>
                </li>
                <li class="list-inline-item g-mr-20">
                  <router-link v-bind:to="{ path: `/blog/${blog.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
                    <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ blog.comments_count }}
                  </router-link>
                </li>
              </ul>
              <ul class="list-inline mb-0 ml-auto">
                
              </ul>
            </div>
          </div>
        </div>

      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="blogs">
      <pagination
        v-bind:cur-page="blogs._meta.page"
        v-bind:per-page="blogs._meta.per_page"
        v-bind:total-pages="blogs._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../../store'
import Blog from '../Base/Blog'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
import Pagination from '../Base/Pagination'

export default {
  name: 'Blogs',  // this is the name of the component
  components: {
    Blog,
    VueMarkdown,
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      blogs: ''
    }
  },
  methods: {
    getUserLikedBlogs (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/liked-blogs/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.blogs = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    const user_id = this.$route.params.id || this.sharedState.user_id
    this.getUserLikedBlogs(user_id)
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    const user_id = to.params.id || this.sharedState.user_id
    this.getUserLikedBlogs(user_id)
  }
}
</script>
