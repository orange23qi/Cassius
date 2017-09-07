<template>
    <b-container>
      <b-row align-h="center"> 
            <b-card bg-variant="dark" text-variant="white" header="注册" class="col-md-6 text-center big-font login-card">
                <b-row align-h="center">
                    <b-form @submit="onSubmit" class="col-md-6 was-validated">
                        <b-form-group id="username"
                                      label="用户名:" label-for="Username" class="text-left">
                            <b-form-input id="Username"
                                        type="text" v-model="form.username" required
                                        placeholder="请输入用户名" />
                        </b-form-group>

                        <b-form-group id="email"
                                      label="邮箱:" label-for="email" class="text-left">
                            <b-form-input id="Email"
                                        type="email" v-model="form.email" required
                                        placeholder="请输入邮箱" />
                        </b-form-group>

                        <b-form-group id="password"
                                      label="密码:" label-for="Password" class="text-left">
                            <b-form-input id="Password"
                                        type="password" v-model="form.password" required
                                        placeholder="请输入密码" />
                        </b-form-group>

                        <b-form-group id="repassword"
                                      label="重复密码:" label-for="repassword" class="text-left">
                            <b-form-input id="Repassword"
                                        type="password" v-model="form.repassword" required
                                        placeholder="请输入重复密码" />
                        </b-form-group>

                        <b-button type="submit" variant="primary">注册</b-button>
                        <b-button type="button" variant="default">
                          <router-link to="/login">立即登录</router-link>
                        </b-button>
                    </b-form>
                </b-row>
            </b-card>
        </b-row>
    </b-container>
</template>
<script>
  export default {
    data(){
      return {
        form: {
          username : '',
          email    : '',
          password : '',
          repassword : '',
          secret: 'S3CR3T'
        }
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        alert(JSON.stringify(this.form));
        this.$http.post('/someUrl', {foo: 'bar'}).then(response => {

            // get status
            response.status;

            // get status text
            response.statusText;

            // get 'Expires' header
            response.headers.get('Expires');

            // get body data
            this.someData = response.body;

          }, response => {
            // error callback
          });
      }
    }
  };
</script>
