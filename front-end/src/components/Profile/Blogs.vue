<template>
  <div>
    <!-- Modal: Edit Blog -->
    <div class="modal fade" id="editBlogModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editBlogModalTitle">Update Blog</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <form id="editBlogForm" @submit.prevent="onSubmitUpdateBlog" @reset.prevent="onResetUpdateBlog">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editBlogForm.titleError}">
                <input type="text" v-model="editBlogForm.title" class="form-control" id="editBlogFormTitle" placeholder="标题">
                <small class="form-control-feedback" v-show="editBlogForm.titleError">{{ editBlogForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editBlogForm.summary" class="form-control" id="editBlogFormSummary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editBlogForm.content" class="form-control" id="editBlogFormContent" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editBlogForm.contentError">{{ editBlogForm.contentError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>
    
          </div>
        </div>
      </div>
    </div>

    <!-- 用户的文章列表 -->
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> User Blogs <small v-if="blogs">(共 {{ blogs._meta.total_items }} 篇, {{ blogs._meta.total_pages }} 页)</small>
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

        <blog v-for="(blog, index) in blogs.items" v-bind:key="index"
          v-bind:blog="blog"
          v-on:edit-blog="onEditBlog(blog)"
          v-on:delete-blog="onDeleteBlog(blog)">
        </blog>

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
import Pagination from '../Base/Pagination'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'Blogs',  // this is the name of the component
  components: {
    Blog,
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      blogs: '',
      editBlogForm: {
        title: '',
        summary: '',
        content: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        contentError: null
      }
    }
  },
  methods: {
  getUserBlogs (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/blogs/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.blogs = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onEditBlog (blog) {
      // 不要使用对象引用赋值： this.editBlogForm = blog
      // 这样是同一个 blog 对象，用户在 editBlogForm 中的操作会双向绑定到该 blog 上， 你会看到 modal 下面的博客也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdateBlog() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
      this.editBlogForm = Object.assign({}, blog)
    },
    onSubmitUpdateBlog () {
      this.editBlogForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editBlogForm .form-control-feedback').remove()
      $('#editBlogForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editBlogForm.title) {
        this.editBlogForm.errors++
        this.editBlogForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editBlogFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editBlogFormTitle').after('<small class="form-control-feedback">' + this.editBlogForm.titleError + '</small>')
      } else {
        this.editBlogForm.titleError = null
      }

      if (!this.editBlogForm.content) {
        this.editBlogForm.errors++
        this.editBlogForm.contentError = 'Content is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blog_content 上
        $('#editBlogForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editBlogForm .md-editor').after('<small class="form-control-feedback">' + this.editBlogForm.contentError + '</small>')
      } else {
        this.editBlogForm.contentError = null
      }

      if (this.editBlogForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#editBlogModal').modal('hide')

      const path = `/api/blogs/${this.editBlogForm.id}`
      const payload = {
        title: this.editBlogForm.title,
        summary: this.editBlogForm.summary,
        content: this.editBlogForm.content
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getUserBlogs(this.$route.params.id || this.sharedState.user_id)
          this.$toasted.success('Successed update the blog.', { icon: 'fingerprint' })
          this.editBlogForm.title = '',
          this.editBlogForm.summary = '',
          this.editBlogForm.content = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onResetUpdateBlog () {
      // 先移除错误
      $('#editBlogForm .form-control-feedback').remove()
      $('#editBlogForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editBlogModal').modal('hide')
      // this.getUserBlogs(this.$route.params.id)
      this.$toasted.info('Cancelled, the blog is not update.', { icon: 'fingerprint' })
    },
    onDeleteBlog (blog) {
      this.$swal({
        title: "Are you sure?",
        text: "该操作将彻底删除 [ " + blog.title + " ], 请慎重",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/blogs/${blog.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this blog', 'success')
              // 必须加个动态参数，不然路由没变化的话，User 组件不会重新执行 getUser()，就不会更新 Blogs 计数
              this.$router.push({ path: this.$route.fullPath, query: { timestamp: Number(new Date()) } })
              // this.getUserBlogs(this.$route.params.id || this.sharedState.user_id)
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
              this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
            })
        } else {
          this.$swal('Cancelled', 'The blog is safe :)', 'error')
        }
      })
    }
  },
  created () {
    const user_id = this.$route.params.id || this.sharedState.user_id
    this.getUserBlogs(user_id)
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#editBlogFormContent").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    const user_id = to.params.id || this.sharedState.user_id
    this.getUserBlogs(user_id)
  }
}
</script>
