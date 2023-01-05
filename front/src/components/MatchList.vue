<template>
	<v-container>
		<v-row class="mt-6 text-center">
			<v-col cols="6" v-for="(match, index) in info" :key="match.id">
				<v-card class="light-green lighten-5 mx-auto" cols="12" max-width="400">
					<v-card-title class="subtitle-1 justify-center pt-1 pb-1">
						{{ index + 1 }}コート
					</v-card-title>
					<v-divider></v-divider>
					<v-card-text>
						<v-row>
							<v-col cols="6" :class="{ 'red--text text--accent-1': match.pair1.player1.sex == 2 }"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair1.player1.name }}
							</v-col>
							<v-col cols="6" :class="{ 'red--text text--accent-1': match.pair1.player2.sex == 2 }"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair1.player2.name }}
							</v-col>
						</v-row>
						<v-row>
							<v-col col="5" class="mt-3 mb-3 pa-0"><v-divider border-width="100" /></v-col>
							<v-col col="1" class="mr-n3 ml-n3 pa-0">vs</v-col>
							<v-col col="5" class="mt-3 mb-3 pa-0"><v-divider /></v-col>
						</v-row>
						<v-row>
							<v-col cols="6" :class="[match.pair2.player1.sex == 2 ? 'red--text text--accent-1' : '']"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair2.player1.name }}
							</v-col>
							<v-col cols="6" :class="[match.pair2.player2.sex == 2 ? 'red--text text--accent-1' : '']"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair2.player2.name }}
							</v-col>
						</v-row>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
		<v-row>
			<v-col class="text-center">
				<v-btn color="light-green" @click="getMatchList">
					試合を組む
				</v-btn>
			</v-col>
		</v-row>
		<v-row>
			<v-col class="text-center">
				<v-btn color="blue-grey lighten-4" :disabled="isMatchConfirmed" @click="confirmMatch">
					試合確定
				</v-btn>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';

export default {
	name: 'MatchList',
	data: () => ({
		isMatchConfirmed: true,
		info: [
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
		],
	}),
	methods: {
		confirmMatch() {
			// TODO: 確定した組み合わせをAPIに投げる
			this.isMatchConfirmed = true;
		},
		getMatchList() {
			axios
				.get('http://localhost:8000')
				.then(res => (this.info = res.data.matchs))
				.catch((error) => console.log(error));
			this.isMatchConfirmed = false;
		}
	}
}
</script>