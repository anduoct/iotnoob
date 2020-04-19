<template>
  <div class="container">

    <!-- Modal: Edit Blog -->
    <div data-backdrop="static" class="modal fade" id="editBlogModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
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

    <form id="addBlogForm" v-if="sharedState.is_authenticated && sharedState.user_perms.includes('write')" @submit.prevent="onSubmitAddBlog" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': blogForm.titleError}">
        <input type="text" v-model="blogForm.title" class="form-control" id="blogFormTitle" placeholder="标题">
        <small class="form-control-feedback" v-show="blogForm.titleError">{{ blogForm.titleError }}</small>
      </div>
      <div class="form-group">
        <input type="text" v-model="blogForm.summary" class="form-control" id="blogFormSummary" placeholder="摘要">
      </div>
      <div class="form-group">
        <textarea v-model="blogForm.content" class="form-control" id="blogFormContent" rows="5" placeholder=" 内容"></textarea>
        <small class="form-control-feedback" v-show="blogForm.contentError">{{ blogForm.contentError }}</small>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Blogs <small v-if="blogs">(共 {{ blogs._meta.total_items }} 篇, {{ blogs._meta.total_pages }} 页)</small>
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
    <div v-if="blogs && blogs._meta.total_pages > 1">
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
import store from '../store'
import Blog from './Base/Blog'
import Pagination from './Base/Pagination'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'Home',  //this is the name of the component
  components: {
    Blog,
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      blogs: '',
      blogForm: {
        title: '',
        summary: '',
        content: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        contentError: null
      },
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
    getBlogs () {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/blogs/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.blogs = response.data
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onSubmitAddBlog (e) {
      this.blogForm.errors = 0  // 重置

      if (!this.blogForm.title) {
        this.blogForm.errors++
        this.blogForm.titleError = 'Title is required.'
      } else {
        this.blogForm.titleError = null
      }

      if (!this.blogForm.content) {
        this.blogForm.errors++
        this.blogForm.contentError = 'Content is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blogFormContent 上
        $('#addBlogForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.blogForm.contentError = null
        $('#addBlogForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.blogForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/blogs'
      const payload = {
        title: this.blogForm.title,
        summary: this.blogForm.summary,
        content: this.blogForm.content
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getBlogs()
          this.$toasted.success('Successed add a new blog.', { icon: 'fingerprint' })
          this.blogForm.title = '',
          this.blogForm.summary = '',
          this.blogForm.content = ''
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.blogForm.titleError = error.response.data.message[field]
            } else if (field == 'content') {
              this.blogForm.contentError = error.response.data.message[field]
            } else {
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
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
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blogFormContent 上
        $('#editBlogForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editBlogForm .md-editor').after('<small class="form-control-feedback">' + this.editBlogForm.contentError + '</small>')
      } else {
        this.editBlogForm.contentError = null
      }

      if (this.editBlogForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/blogs/${this.editBlogForm.id}`
      const payload = {
        title: this.editBlogForm.title,
        summary: this.editBlogForm.summary,
        content: this.editBlogForm.content
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // 先隐藏 Modal
          $('#editBlogModal').modal('hide')

          // handle success
          this.getBlogs()
          this.$toasted.success('Successed update the blog.', { icon: 'fingerprint' })
          this.editBlogForm.title = '',
          this.editBlogForm.summary = '',
          this.editBlogForm.content = ''
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.editBlogForm.titleError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              $('#editBlogFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editBlogFormTitle').after('<small class="form-control-feedback">' + this.editBlogForm.titleError + '</small>')
            } else if (field == 'content') {
              this.editBlogForm.contentError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blogFormContent 上
              $('#editBlogForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editBlogForm .md-editor').after('<small class="form-control-feedback">' + this.editBlogForm.contentError + '</small>')
            } else {
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
        })
    },
    onResetUpdateBlog () {
      // 先移除错误
      $('#editBlogForm .form-control-feedback').remove()
      $('#editBlogForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editBlogModal').modal('hide')
      // this.getBlogs()
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
              // this.$toasted.success('Successed delete the blog.', { icon: 'fingerprint' })
              this.getBlogs()
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
    this.getBlogs()
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#blogFormContent, #editBlogFormContent").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当查询参数 page 或 per_page 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    // 注意：要先执行 next() 不然 this.$route.query 还是之前的
    next()
    this.getBlogs()
  }
}
</script>