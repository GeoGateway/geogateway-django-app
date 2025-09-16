<template>
  <div class="w-100 window">
    <q-toolbar class="navbar-custom" id="top">
      <!-- Logo always visible -->
      <q-toolbar-title class="pl-3">
        <img id="logo" src="../assets/LogoDark.png" alt="GeoGateway Logo" @click="move_logo_right">
      </q-toolbar-title>

      <q-space />

      <!-- Desktop: Always show buttons -->
      <div v-if="$q.screen.gt.sm" class="q-gutter-sm">
        <q-btn flat color="secondary" @click="feedbackPopup=true">Feedback</q-btn>
        <q-btn flat color="secondary" @click="helpPopup=true">Help</q-btn>
        <q-btn outline color="primary" href="/auth/login">
          <q-icon name="account_circle" left />Login
        </q-btn>
      </div>

      <!-- Mobile: Show hamburger menu -->
      <q-btn v-else flat round icon="menu" @click="mobileMenuOpen = !mobileMenuOpen" />
    </q-toolbar>

    <!-- Mobile drawer menu -->
    <q-drawer v-model="mobileMenuOpen" side="right" overlay>
      <q-list>
        <q-item clickable @click="feedbackPopup=true; mobileMenuOpen=false">
          <q-item-section>Feedback</q-item-section>
        </q-item>
        <q-item clickable @click="helpPopup=true; mobileMenuOpen=false">
          <q-item-section>Help</q-item-section>
        </q-item>
        <q-item clickable tag="a" href="/auth/login">
          <q-item-section avatar>
            <q-icon name="account_circle" />
          </q-item-section>
          <q-item-section>Login</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <!-- feedback  popup -->
    <q-dialog v-model="feedbackPopup">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Feed Back</div>
        </q-card-section>
        <q-card-section>
          <report/>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" @click="feedbackPopup = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- help  popup -->
    <q-dialog v-model="helpPopup">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Help</div>
        </q-card-section>
        <q-card-section>
          <help/>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" @click="helpPopup = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </div>
</template>

<script>
// import ToolBar from "./ToolBar";
import report from "./report"
import help from "./help"

export default {
  name: "TopNav",
  components: {
    // ToolBar
    report,
    help,
  },
  data() {
    return {
      feedbackPopup: false,
      helpPopup: false,
      mobileMenuOpen: false,
    };
  },
  methods: {
    loginRoute() {

    },
    move_logo_right: function () {
      var step = 50;
      var y = document.getElementById('logo').offsetLeft;
      y = y + step;
      document.getElementById('logo').style.left = y + "px";
    }
  }
}
</script>

<style scoped lang="scss">

//.navbar-custom {
//  height: 40px;
//  background: $white;
//  justify-content: right;
//}
//
.window {
  background: white;
  box-shadow: 1px 1px 1px 1px rgba(108, 117, 125, 0.3);
  z-index: 99999;
}

//
#logo {
  //  position: absolute;
  //  left: 0%;
  //  right: 0%;
  //  top: 0%;
  //  bottom: 0%;
  //
  //  float: left;
  height: 30px;
  width: 100px;
}

//
//#login {
//  color: #2F7CF6;
//  background: #FFFFFF;
//  border: 1px solid #A2B8BF;
//  box-sizing: border-box;
//  border-radius: 5px;
//  display: flex;
//  align-items: flex-start;
//
//  font-style: normal;
//  font-weight: 600;
//  font-size: 16px;
//  line-height: 19px;
//  display: flex;
//  align-items: center;
//
//}
//
//.miscButton {
//  background: none;
//  border: none;
//  font-style: normal;
//  font-weight: 600;
//  font-size: 16px;
//  line-height: 19px;
//  display: flex;
//  align-items: center;
//  margin-left: 20px;
//  margin-right: 20px;
//  float: right;
//  /* Primary text colour */
//
//  color: #283237;
//}
</style>
