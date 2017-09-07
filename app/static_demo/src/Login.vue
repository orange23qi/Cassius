<template>
    <b-container>
      <b-row align-h="center"> 
            <b-card bg-variant="dark" text-variant="white" header="登录" class="col-md-6 text-center big-font login-card">
                <b-row align-h="center">
                    <b-form @submit="onSubmit" class="col-md-6 was-validated">
                        <b-form-group id="username"
                                      label="用户名:" label-for="Username" class="text-left">
                            <b-form-input id="Username"
                                        type="text" v-model="form.username" required
                                        placeholder="请输入用户名" />
                        </b-form-group>

                        <b-form-group id="password"
                                      label="密码:" label-for="Password" class="text-left">
                            <b-form-input id="Password"
                                        type="password" v-model="form.password" required
                                        placeholder="请输入密码" />
                        </b-form-group>
                        <b-button type="submit" variant="primary">登录</b-button>
                        <b-button type="button" variant="default">
                          <router-link to="/register">立即注册</router-link>
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
          username: '',
          password: '',
          checked: false,
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
