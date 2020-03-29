<template>
  <section>
    <!-- Modal: Send Message -->
    <div class="modal fade" id="sendMessageModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="sendMessageModalTitle">Send Private Message</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <form id="sendMessageForm" @submit.prevent="onSubmitSendMessage" @reset.prevent="onResetSendMessage">
              <div class="form-group">
                <textarea v-model="sendMessageForm.content"  class="form-control" id="sendMessageFormContent" rows="5" placeholder=" 悄悄话..."></textarea>
                <small class="form-control-feedback" v-show="sendMessageForm.contentError">{{ sendMessageForm.contentError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
    
          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Send Message -->

    <!-- 用户信息 -->
    <div v-if="user" class="container">
      <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
        <div class="row">
          <div class="col-sm-3 g-mb-40 g-mb-0--lg">
            <!-- User Image -->
            <div class="g-mb-20">
              <img v-if="user._links.avatar" class="img-fluid w-100" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username">
            </div>
            <!-- User Image -->

            <!-- Actions -->
            <button v-if="!user.is_following && $route.params.id != sharedState.user_id" v-on:click="onFollowUser($route.params.id)" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> Follow
            </button>

            <button v-if="user.is_following && $route.params.id != sharedState.user_id" v-on:click="onUnfollowUser($route.params.id)" class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-unfollow g-pos-rel g-top-1 g-mr-5"></i> Unfollow
            </button>

            <button v-if="$route.params.id != sharedState.user_id" class="btn btn-block u-btn-outline-aqua g-rounded-50 g-py-12 g-mb-10" data-toggle="modal" data-target="#sendMessageModal">
              <i class="icon-envelope g-pos-rel g-top-1 g-mr-5"></i> Send private message
            </button>

            <router-link v-if="$route.params.id == sharedState.user_id" v-bind:to="{ name: 'SettingProfile' }" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
            </router-link>

            <button v-if="$route.params.id == sharedState.user_id" v-on:click="onDeleteUser($route.params.id)" class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-ban g-pos-rel g-top-1 g-mr-5"></i> Delete Your Account
            </button>
            <!-- End Actions -->
           
          </div>

          <div class="col-sm-9">

            <!-- Tab Nav -->
            <ul class="nav nav-tabs g-mb-20">
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserOverview' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="isUserOverView">Overview <span class="u-label g-font-size-11 g-bg-primary g-rounded-20 g-px-10"><i class="icon-layers g-pos-rel g-top-1 g-mr-8"></i></span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowers' }" v-bind:active-class="'active'" class="nav-link">Followers <span class="u-label g-font-size-11 g-bg-deeporange g-rounded-20 g-px-10">{{ user.followers_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowing' }" v-bind:active-class="'active'" class="nav-link">Following <span class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">{{ user.followeds_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserBlogs' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="{'active': $route.name == 'UserFollowingBlogs'}">Blogs <span class="u-label g-font-size-11 g-bg-purple g-rounded-20 g-px-10">{{ user.blogs_count }}</span></router-link>
              </li>
            </ul>

            <!-- 嵌套的子路由出口 -->
            <router-view></router-view>

          </div>
        </div>
      </div>
    </div>

    <!-- 当前登录的用户发表新博客文章 -->
    <div class="container">

      <div v-if="sharedState.is_authenticated && $route.params.id == sharedState.user_id" class="card border-0 g-mb-15">
        <!-- Panel Header -->
        <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
          <h3 class="h6 mb-0">
            <i class="icon-fire g-pos-rel g-top-1 g-mr-5"></i> Publish New Blog
          </h3>
          <div class="dropdown g-mb-10 g-mb-0--md">
            <span class="d-block g-mr-minus-5 g-pa-5">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
          </div>
        </div>
        <!-- End Panel Header -->
      </div>

      <form id="addBlogForm" v-if="sharedState.is_authenticated && $route.params.id == sharedState.user_id" @submit.prevent="onSubmitAddBlog" class="g-mb-40">
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

    </div>
  </section>
</template>

<script>
import store from '../../store'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'User',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      user: '',
      blogForm: {
        title: '',
        summary: '',
        content: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        contentError: null
      }, 
      sendMessageForm: {
        content: '',
        errors: 0,  // 发送站内消息时，表单验证是否有错误
        contentError: null
      }
    }
  },
  computed: {
    isUserOverView: function () {
      const tabs = ['UserFollowers', 'UserFollowing', 'UserBlogs', 'UserFollowingBlogs']
      if (tabs.indexOf(this.$route.name) == -1) {
        return 'active'
      } else {
        return ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onFollowUser (id) {
      const path = `/api/follow/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onUnfollowUser (id) {
      const path = `/api/unfollow/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onDeleteUser (id) {
      this.$swal({
        title: "Are you sure ?",
        text: "Please provide your password.",
        input: 'password',
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        inputValidator: (value) => {
          return !value && 'Please provide a valid password.'
        }
      }).then((result) => {
        if (result.value) {
          const path = '/api/tokens'
          // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
          this.$axios.post(path, {}, {
            auth: {
              'username': this.user.username,
              'password': result.value
            }
          }).then((response) => {
              // handle success
              const path = `/api/users/${id}`
              this.$axios.delete(path)
                .then((response) => {
                  // handle success
                  this.$swal('Deleted', 'You are anonymous now, Goodby!', 'success')
                  store.logoutAction()
                  this.user = ''
                  this.$router.push('/')
                })
                .catch((error) => {
                  // handle error
                  console.log(error.response.data)
                  this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
                })
            })
            .catch((error) => {
              // handle error
              this.$toasted.error('Invalid password, you cannot delete this account.', { icon: 'fingerprint' })
              console.error('Invalid password, you cannot delete this account.')
            })
        } else {
          this.$swal('Cancelled', 'Your account is safe :)', 'error')
        }
      })
    },
    onSubmitSendMessage () {
      this.sendMessageForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#sendMessageForm .form-control-feedback').remove()
      $('#sendMessageForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.sendMessageForm.content) {
        this.sendMessageForm.errors++
        this.sendMessageForm.contentError = 'Content is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blog_content 上
        $('#sendMessageForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#sendMessageForm .md-editor').after('<small class="form-control-feedback">' + this.sendMessageForm.contentError + '</small>')
      } else {
        this.sendMessageForm.contentError = null
      }

      if (this.sendMessageForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#sendMessageModal').modal('hide')

      const payload = {
        recipient_id: this.$route.params.id,
        content: this.sendMessageForm.content
      }
      this.$axios.post('/api/messages/', payload)
        .then((response) => {
          // handle success
          this.$toasted.success(`Successed send the private message to ${this.user.username}.`, { icon: 'fingerprint' })
          this.sendMessageForm.content = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onResetSendMessage () {
      // 先移除错误
      $('#sendMessageForm .form-control-feedback').remove()
      $('#sendMessageForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#sendMessageModal').modal('hide')
      // this.getBlogs()
      this.$toasted.info(`Cancelled, no words send to ${this.user.username}.`, { icon: 'fingerprint' })
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
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #blog_content 上
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.blogForm.contentError = null
        $('.md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.blogForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/blogs/'
      const payload = {
        title: this.blogForm.title,
        summary: this.blogForm.summary,
        content: this.blogForm.content
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed add a new blog.', { icon: 'fingerprint' })
          this.blogForm.title = '',
          this.blogForm.summary = '',
          this.blogForm.content = ''
          // 必须加个动态参数，不然路由没变化的话，UserBlogsList 组件不会刷新重新加载博客列表
          this.$router.push({ name: 'UserBlogsList', query: { id: response.data.id } })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    }
  },
  created () {
    const user_id = this.$route.params.id
    this.getUser(user_id)
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#blogFormContent, #sendMessageFormContent").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUser(to.params.id)
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#blogFormContent, #sendMessageFormContent").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  }
}
</script>
